// Grava os quadros do vídeo do topo do site a partir do configurador (?filme).
// Uso: node ferramentas/filme.js <pasta-de-saída> [fps=30] [largura=1280] [altura=720] [tomadas=0,1,2] [passo=1]
//   Precisa do site servido em http://localhost:8765 (cd site && python3 -m http.server 8765) e do Playwright.
//   THREE_DIR=<pasta do pacote three@0.160.0> serve o three.js local quando o CDN não está acessível.
// Depois: ferramentas/filme.sh <pasta-de-saída> monta site/video/heroi.mp4, heroi.webm e o pôster.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const [out, fps = 30, W = 1280, H = 720, tom = '0,1,2', passo = 1] = process.argv.slice(2);
const SOBRA = 0.5;   // meio segundo extra no fim de cada tomada para a transição
(async () => {
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: +W, height: +H } });
  p.on('pageerror', e => console.log('PAGEERR', e.message));
  if (process.env.THREE_DIR) await p.route(/cdn\.jsdelivr\.net\/npm\/three@0\.160\.0\/(.*)/, r => {
    const f = path.join(process.env.THREE_DIR, r.request().url().match(/three@0\.160\.0\/(.*)/)[1]);
    fs.existsSync(f) ? r.fulfill({ path: f, contentType: 'application/javascript' }) : r.fulfill({ status: 404 }); });
  await p.route(/fonts\.(googleapis|gstatic)/, r => r.fulfill({ status: 200, body: '' }));
  // o laço de animação da página fica parado: cada quadro é desenhado só por __quadro
  await p.route(/configurador\.html/, async r => {
    const res = await r.fetch(); let t = await res.text();
    t = t.replace('function loop(now){\n  requestAnimationFrame(loop);', 'function loop(now){\n  requestAnimationFrame(loop); if(window.__pare) return;')
         .replace('<script type="module">', '<script>window.__pare=true;</script><script type="module">');
    r.fulfill({ response: res, body: t, headers: { 'content-type': 'text/html' } }); });
  await p.goto('http://localhost:8765/configurador.html?filme', { waitUntil: 'load' });
  await p.waitForFunction(() => document.title === 'PRONTO', null, { timeout: 300000 });
  await p.waitForTimeout(1000);
  const durs = await p.evaluate(() => window.__TOMADAS);
  for (const i of tom.split(',').map(Number)) {
    const n = Math.round((durs[i] + SOBRA) * fps);
    for (let f = 0; f < n; f += +passo) {
      await p.evaluate(([i, t]) => window.__quadro(i, t), [i, f / fps]);
      await p.waitForTimeout(150);
      await p.screenshot({ path: path.join(out, `t${i}_${String(f).padStart(4, '0')}.png`), timeout: 180000 });
      if (f % 15 === 0) console.log(`tomada ${i}: ${f + 1}/${n}`);
    }
  }
  await b.close();
})();
