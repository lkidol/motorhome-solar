import base64, json, os, pathlib, re, subprocess

SITE = pathlib.Path(__file__).resolve().parent
ROOT = SITE.parent
DADOS = ROOT / 'dados'
MODELOS = SITE / 'modelos'

src = (SITE / 'index.html').read_text(encoding='utf-8')
# module script body
a = src.index('<script type="module">'); b = src.index('</script>', a)
js = src[a + len('<script type="module">'):b]
js = js.replace("from 'three/addons/", "from 'three/examples/jsm/")
js = js.replace(
    "const r = await fetch('malha.json').then(x=>x.ok?x:fetch('../dados/malha.json')); const d = await r.json();",
    "const d = DADO('malha');",
)
js = js.replace(
    "['detalhes.json','relevos.json'].map(async f=>{ try{ return await (await fetch(f).then(x=>x.ok?x:fetch('../dados/'+f))).json(); }catch(e){ console.error(f,e); return []; } })",
    "['detalhes','relevos'].map(async f=>{ try{ return DADO(f); }catch(e){ console.error(f,e); return []; } })",
)
js = js.replace(
    "let _modelos=null; async function bufModelo(arq){ _modelos??=fetch('modelos.json').then(r=>r.json()); const t=(await _modelos)[arq]; const bin=atob(t); const u=new Uint8Array(bin.length); for(let i=0;i<bin.length;i++) u[i]=bin.charCodeAt(i); return u.buffer; }",
    "async function bufModelo(arq){ const t=document.getElementById('m-'+arq).textContent.trim(); const bin=atob(t); const u=new Uint8Array(bin.length); for(let i=0;i<bin.length;i++) u[i]=bin.charCodeAt(i); return u.buffer; }",
)
assert 'fetch(' not in js
if os.environ.get('TESTE'):
    js += '\n' + (SITE / 'debug.js').read_text(encoding='utf-8')
js = "const DADO=id=>JSON.parse(document.getElementById('d-'+id).textContent);\n" + js
(SITE / 'main.js').write_text(js, encoding='utf-8')
esbuild = SITE / 'node_modules' / '.bin' / ('esbuild.cmd' if os.name == 'nt' else 'esbuild')
subprocess.run([str(esbuild), 'main.js', '--bundle', '--minify', '--format=esm', '--target=es2020', '--outfile=bundle.js'], cwd=SITE, check=True)
bun = (SITE / 'bundle.js').read_text(encoding='utf-8')
assert '</script' not in bun.lower()
# html head/body without importmap, module and google fonts
im0 = src.index('<script type="importmap">'); im1 = src.index('</script>', im0) + len('</script>')
html = src[:im0] + src[im1:a]
html = re.sub(r'<link rel="preconnect"[^>]*>\n?', '', html)
html = re.sub(r'<link href="https://fonts.googleapis.com[^>]*>\n?', '', html)
dados = ''
for k, f in [('malha', 'malha.json'), ('detalhes', 'detalhes.json'), ('relevos', 'relevos.json')]:
    t = (DADOS / f).read_text(encoding='utf-8'); json.loads(t)
    dados += f'<script type="application/json" id="d-{k}">{t}</script>\n'
for f in sorted(MODELOS.glob('*.glb')):
    dados += f'<script type="application/octet-stream" id="m-{f.stem}">' + base64.b64encode(f.read_bytes()).decode() + '</script>\n'
out = html + dados + '<script type="module">\n' + bun + '\n</script>\n' + src[b + len('</script>'):]
out_path = SITE / ('teste_3d.html' if os.environ.get('TESTE') else 'motorhome_solar_3d.html')
out_path.write_text(out, encoding='utf-8')
print(len(out) / 1e6, 'MB')
