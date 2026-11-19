p='/home/claude/motorhome/index.html'; s=open(p,encoding='utf-8').read()
part=open('/home/claude/motorhome/interacoes.js.part',encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:80]); s=s.replace(a,b)
# move registry defs earlier
part=part.replace("const LUZ={};\nfunction regLuz(k,m){ (LUZ[k]=LUZ[k]||[]).push(m); }\n","")
rep("const MATS_DET = {","const LUZ={};\nfunction regLuz(k,m){ (LUZ[k]=LUZ[k]||[]).push(m); }\nconst MATS_DET = {")
# register detail lights
rep("        o.g.add(mesh); pickables.push(mesh); o.mats.push(mat); if(d.mat==='lente') mat.userData.op=0.3;",
    "        o.g.add(mesh); pickables.push(mesh); o.mats.push(mat); if(d.mat==='lente') mat.userData.op=0.3;\n        regLuz(d.id+':'+d.mat,mat);")
# modules: per-module light material
rep("""    const disco=new THREE.Mesh(new THREE.CircleGeometry(mo.r*0.78,28),luz);""",
"""    const lz=luz.clone(); regLuz('farol:'+mo.nome,lz);
    const disco=new THREE.Mesh(new THREE.CircleGeometry(mo.r*0.78,28),lz);""")
# door hinge & handle
rep('"forma": "porta", "furo": "casa", "vidroH": 1.4,','"forma": "porta", "furo": "casa", "vidroH": 1.4, "dobradica": "tras",')
rep("mac.position.copy(W(c.s[1]-0.16,lado*(xw+0.004),1.06)); g.push(mac);",
    "mac.position.copy(W(c.dobradica==='tras'?c.s[0]+0.16:c.s[1]-0.16,lado*(xw+0.004),1.06)); g.push(mac);")
# mats filter
rep("const mats=[...new Set(parts.map(p=>p.material))].filter(m=>m!==vidroMat);","const mats=[...new Set(parts.map(p=>p.material))].filter(m=>m&&m!==vidroMat);")
# info card action
rep("  if(focar) flyTo(null,o.center);","""  if(ABRE[id]){ const b=document.createElement('button'); b.className='acao'; b.textContent=ABRE[id].alvo>0.5?'Fechar':'Abrir'; b.addEventListener('click',()=>abre(id)); info.appendChild(b); }
  if(focar) flyTo(null,o.center);""")
# pointerup in FP
rep("  if(hit) select(hit.object.userData.comp.id,false); else { if(selId) select(null); }\n});",
"""  if(FP.on){ const id=hit?.object.userData.comp?.id; if(id&&ABRE[id]) abre(id); return; }
  if(hit) select(hit.object.userData.comp.id,false); else { if(selId) select(null); }
});""")
# presets
rep("const presetBtns=['p-ext','p-geral','p-interior','p-tecnico','p-estac']","const presetBtns=['p-ext','p-geral','p-interior','p-tecnico','p-estac','p-camp']")
rep("  presetBtns.forEach(b=>b.setAttribute('aria-pressed',b.id===id));",
    "  if(FP.on){ FP.on=false; controls.enabled=true; camera.near=0.05; document.body.classList.remove('dentro'); syncUI(); }\n  presetBtns.forEach(b=>b.setAttribute('aria-pressed',b.id===id));")
rep("  if(id==='p-estac'){","""  if(id==='p-camp'){ setOpacity(100); setCut(250); numerosEl.checked=false; aberturaAlvo=1; setNoite(true);
    Object.assign(EST,{interna:true,toldoLuz:true,posicao:true,farol:'off'}); abre('toldo',true); abre('portaCasa',true); abre('janela',true);
    setView('3d',new THREE.Vector3(0.6,1.0,-1.4),new THREE.Vector3(2.2,3.1,-11.2)); syncUI(); }
  if(id==='p-estac'){""")
rep('<button id="p-estac">Estacionado</button>','<button id="p-estac">Estacionado</button>\n    <button id="p-camp">Acampamento</button>')
# loop
rep("""function loop(now){
  requestAnimationFrame(loop); stepAnim(now);""","""let tAnt=performance.now();
function loop(now){
  requestAnimationFrame(loop); const dt=Math.min(0.05,(now-tAnt)/1000); tAnt=now;
  if(!FP.on) stepAnim(now);
  animaInteracoes(now,dt); aplicaLuzes(now); if(FP.on) andaFP(dt);""")
rep("  controls.update(); renderer.render(scene,camera); updateLabels(); calcOclusao(now); updateTags();",
    "  if(!FP.on) controls.update(); renderer.render(scene,camera); if(!FP.on){ updateLabels(); calcOclusao(now); updateTags(); }")
# insert interaction block
rep("requestAnimationFrame(loop);\nconst paintsEl", part+"\nrequestAnimationFrame(loop);\nconst paintsEl")
# HTML: UI section first in aside
rep("""  <aside>
    <section>
      <h2>Vista</h2>""","""  <aside>
    <section id="ui">
      <h2>Interagir</h2>
      <button id="entrar" class="grande">Entrar no motorhome</button>
      <div class="sub2">Abrir e fechar</div>
      <div class="row">
        <button data-abre="portaE">Porta do motorista</button>
        <button data-abre="portaD">Porta do passageiro</button>
        <button data-abre="portaCasa">Porta de entrada</button>
        <button data-abre="janela">Janela da sala</button>
        <button data-abre="toldo">Toldo</button>
      </div>
      <div class="sub2">Luzes</div>
      <div class="row"><button id="noite">Noite</button><button data-luz="interna">Luz interna</button><button data-luz="toldoLuz">Luz do toldo</button></div>
      <div class="row seg" role="group" aria-label="Faróis"><span>Faróis</span><button data-farol="off">Desligados</button><button data-farol="baixo">Baixo</button><button data-farol="alto">Alto</button></div>
      <div class="row"><button data-luz="drl">Luz diurna</button><button data-luz="posicao">Lanternas</button><button data-luz="freio">Freio</button><button data-luz="re">Ré</button></div>
      <div class="row"><button data-luz="setaE">◀ Seta</button><button data-luz="alerta">Pisca-alerta</button><button data-luz="setaD">Seta ▶</button></div>
      <div class="sub2">Outros</div>
      <div class="row"><button data-luz="limp">Limpadores</button></div>
      <p class="note" style="margin-top:8px">Também dá para clicar numa porta, na janela ou no toldo e usar o botão Abrir no cartão. Os painéis solares e o degrau estão em Vista.</p>
    </section>
    <section>
      <h2>Vista</h2>""")
rep("""    <div id="err">""","""    <div id="fp">
      <div class="fp-top">
        <b>Dentro do motorhome</b>
        <div class="lugares" role="group" aria-label="Ir para"></div>
        <button id="fp-sair">Sair</button>
      </div>
      <div class="mira" aria-hidden="true"></div>
      <div class="pad" role="group" aria-label="Andar">
        <button data-mv="t:1" aria-label="Virar à esquerda">↺</button>
        <button data-mv="f:1" aria-label="Andar para a frente">▲</button>
        <button data-mv="t:-1" aria-label="Virar à direita">↻</button>
        <span></span>
        <button data-mv="f:-1" aria-label="Andar para trás">▼</button>
      </div>
      <div class="fp-dica">arraste para olhar · ▲▼ ou W A S D para andar · toque numa porta ou na janela para abrir</div>
    </div>
    <div id="err">""")
# CSS
rep(".acab{margin:8px 0 0;",""".grande{width:100%;padding:10px;font-weight:600;font-size:14px;margin-bottom:4px;background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}
.sub2{font:600 12px var(--display);color:var(--muted);margin:10px 0 6px}
#ui .row+.row{margin-top:6px}
.seg span{font-size:13px;color:var(--muted);align-self:center;margin-right:2px}
#info .acao{justify-self:start;margin-top:4px}
#fp{display:none;position:absolute;inset:0;pointer-events:none}
body.dentro #fp{display:block}
body.dentro #labels, body.dentro .stats, body.dentro #info, body.dentro .hint{display:none}
#fp .fp-top{position:absolute;top:10px;left:10px;right:10px;display:flex;gap:8px;align-items:center;flex-wrap:wrap;pointer-events:auto;background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:8px 10px}
#fp .fp-top b{font-size:13px;margin-right:4px}
#fp .lugares{display:flex;gap:6px;flex-wrap:wrap;flex:1}
#fp .lugares button,#fp-sair{padding:5px 9px;font-size:12px}
#fp-sair{background:var(--ink);color:var(--bg);border-color:var(--ink)}
#fp .mira{position:absolute;left:50%;top:50%;width:6px;height:6px;margin:-3px;border-radius:50%;background:rgba(255,255,255,.85);box-shadow:0 0 0 1px rgba(0,0,0,.4)}
#fp .pad{position:absolute;right:14px;bottom:14px;display:grid;grid-template-columns:repeat(3,48px);gap:6px;pointer-events:auto}
#fp .pad button{height:48px;font-size:18px;background:var(--panel);touch-action:none;user-select:none;-webkit-user-select:none}
#fp .fp-dica{position:absolute;left:12px;bottom:14px;max-width:calc(100% - 200px);font-size:12px;color:var(--muted);background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:4px 8px}
@media (max-width:820px){ #fp .fp-dica{display:none} }
.acab{margin:8px 0 0;""")
rep("carcaça.stl · 7,00 × 2,29 × 2,20 m · v7 de 17/11/2026","carcaça.stl · 7,00 × 2,29 × 2,20 m · v8 de 17/11/2026")
open(p,'w',encoding='utf-8').write(s); print('ok')
