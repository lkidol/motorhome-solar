import json
p='/home/claude/motorhome/index.html'; s=open(p,encoding='utf-8').read()
part=open('/home/claude/motorhome/interior.js.part',encoding='utf-8').read().replace('__LED_LOOP__',open('/home/claude/geo/led_loop.json').read())
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:80]); s=s.replace(a,b)
rep("import { RoomEnvironment }","import { RoomEnvironment }",0) if False else None
rep("import { toCreasedNormals } from 'three/addons/utils/BufferGeometryUtils.js';",
    "import { toCreasedNormals } from 'three/addons/utils/BufferGeometryUtils.js';\nimport { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';")
# rounded boxAt
rep("""function boxAt(s0,s1,x0,x1,h0,h1,mat){
  const m=new THREE.Mesh(new THREE.BoxGeometry(s1-s0,h1-h0,x1-x0),mat);""","""function boxAt(s0,s1,x0,x1,h0,h1,mat,r){
  const a=s1-s0,b=h1-h0,c=x1-x0, rr=Math.min(r??0.02,Math.min(a,b,c)*0.48);
  const m=new THREE.Mesh(rr>0.0012?new RoundedBoxGeometry(a,b,c,3,rr):new THREE.BoxGeometry(a,b,c),mat);""")
# interior builders after compObj decl
rep("const compObj = {};","const compObj = {};\n"+part)
# dispatch builders
rep("  if(c.forma==='malha'){","  if(BUILD[c.id]||BUILD[c.forma]){\n    parts.push(...(BUILD[c.id]||BUILD[c.forma])(c));\n  } else if(c.forma==='malha'){")
# components: new console and rear lockers; remove old edges
rep('  {"id": "piso", "grupo": "interior",','''  {"id": "console", "grupo": "cabine", "nome": "Console central (porta-copos, carregador, seletor)", "s": [1.52, 2.42], "x": [-0.17, 0.17], "h": [0.30, 0.88], "nota": "Liga o painel ao chão entre os bancos. Apoio de braço estofado atrás, porta-copos e carregador sem fio na frente."},
  {"id": "piso", "grupo": "interior",''')
rep('  {"id": "cama", "grupo": "interior",','''  {"id": "arm_tras", "grupo": "interior", "nome": "Armários sobre o pé da cama (3 portas)", "s": [6.60, 6.93], "x": [-0.80, 0.80], "h": [1.50, 1.86], "nota": "Na parede de trás, atrás da cama. Conferido contra o teto inclinado (1,90 m em 6,9 m)."},
  {"id": "cama", "grupo": "interior",''')
rep("const mats=[...new Set(parts.map(p=>p.material))].filter(m=>m&&m!==vidroMat);",
"""const meshes=[]; g.traverse(o=>{ if(o.isMesh&&!parts.includes(o)){ o.userData.comp=c; pickables.push(o); } if(o.isMesh) meshes.push(o); });
  const mats=[...new Set(meshes.flatMap(p=>Array.isArray(p.material)?p.material:[p.material]))].filter(m=>m&&m!==vidroMat&&m!==fitaMat);""")
rep("&&p.material!==vidroMat&&p.geometry.type==='BoxGeometry') edges.push(addEdges(p)); }","&&false) edges.push(addEdges(p)); }")
# paint shader: interior lining
rep("function matPintura(){","function matPintura(modo=0){")
rep("    Object.assign(sh.uniforms,PINT_U);","    Object.assign(sh.uniforms,PINT_U,FORRO_U); sh.uniforms.uModo={value:modo};")
rep("sh.vertexShader=sh.vertexShader.replace('#include <common>','#include <common>\\nvarying vec3 vWP;')\n      .replace('#include <project_vertex>','#include <project_vertex>\\nvWP=(modelMatrix*vec4(transformed,1.0)).xyz;');",
    "sh.vertexShader=sh.vertexShader.replace('#include <common>','#include <common>\\nvarying vec3 vWP; varying vec3 vWN;')\n      .replace('#include <project_vertex>','#include <project_vertex>\\nvWP=(modelMatrix*vec4(transformed,1.0)).xyz; vWN=normalize(mat3(modelMatrix)*objectNormal);');")
rep("varying vec3 vWP; uniform vec3 uBody,uFriso,uClad,uPreto; uniform float uMetal;\nfloat zClad,zPreto,zFriso;",
    "varying vec3 vWP; varying vec3 vWN; uniform vec3 uBody,uFriso,uClad,uPreto,uForro,uForroJ,uParede,uCabI,uChaoI; uniform float uMetal,uModo;\nfloat zClad,zPreto,zFriso,zDentro;")
rep("""  c = mix(c,uClad*gr,zClad);
  diffuseColor.rgb = c; }`)""","""  c = mix(c,uClad*gr,zClad);
  bool dentro = uModo>5.0 ? false : (uModo==0.0 ? !gl_FrontFacing : dot(vWN,vec3(0.0,0.0,uModo))<0.0);
  zDentro = dentro ? 1.0 : 0.0;
  if(dentro){
    vec3 on = uModo==0.0 ? vWN : -vWN;
    float fe = 0.95+0.10*h2(floor(vWP.xy*260.0)+floor(vWP.zz*260.0));
    if(on.y>0.55){ c = mix(uForroJ,uForro,step(0.06,fract(s/0.095))) * (0.96+0.08*h2(vec2(floor(s/0.095),3.0))); }
    else if(on.y<-0.55){ c = uChaoI; }
    else { c = (s<2.0 ? uCabI : uParede)*fe; if(s>=2.0 && h<0.36) c=uCabI; }
    zClad=0.0; zPreto=0.0; zFriso=0.0;
  }
  diffuseColor.rgb = c; }`)""")
rep("roughnessFactor = zClad>0.5 ? 0.88 : (zPreto>0.5 ? 0.12 : 0.32);`)","roughnessFactor = zDentro>0.5 ? 0.92 : (zClad>0.5 ? 0.88 : (zPreto>0.5 ? 0.12 : 0.32));`)")
rep("metalnessFactor = zClad>0.5 ? 0.0 : (zPreto>0.5 ? 0.2 : (zFriso>0.5 ? 0.6 : uMetal));`)","metalnessFactor = zDentro>0.5 ? 0.0 : (zClad>0.5 ? 0.0 : (zPreto>0.5 ? 0.2 : (zFriso>0.5 ? 0.6 : uMetal)));`)")
rep("material.clearcoat *= (1.0-zClad);`);","material.clearcoat *= (1.0-zClad)*(1.0-zDentro);`);")
rep("const pinturaMats=[];","""const pinturaMats=[];
const FORRO_U={ uForro:{value:new THREE.Color('#e6dac6')}, uForroJ:{value:new THREE.Color('#8d7457')}, uParede:{value:new THREE.Color('#cdc6bb')},
  uCabI:{value:new THREE.Color('#3a3e42')}, uChaoI:{value:new THREE.Color('#3b3732')} };""")
rep("parts.push(...fazPorta(c,matPintura()));","parts.push(...fazPorta(c,matPintura(Math.sign(c.x[0]+c.x[1]))));")
rep("  pint:     ()=>matPintura(),","  pint:     ()=>matPintura(9),")
# LED lights: replace plafons
a=s.index("const INTERNAS=["); b=s.index("/* ---- toldo: lona listrada")
s=s[:a]+"""const INTERNAS=[ {s:2.45,x:0.78}, {s:3.95,x:0.70}, {s:5.65,x:0.70}, {s:2.45,x:-0.78}, {s:3.95,x:-0.80}, {s:5.65,x:-0.70}, {s:4.22,x:0.56,h:1.95} ];
const fitaLoop=fita(FITA_LOOP,true,0.0075); layers.interior.add(fitaLoop);
const rodape=[ fita([[2.76,0.505,0.315],[3.72,0.505,0.315]],false,0.005), fita([[3.78,-0.465,0.315],[4.12,-0.465,0.315]],false,0.005), fita([[4.68,-0.55,0.315],[5.08,-0.55,0.315]],false,0.005) ];
rodape.forEach(m=>layers.interior.add(m));
const luzesInt=INTERNAS.map(p=>{ const h=p.h ?? (roofH(p.s)-0.22);
  const l=new THREE.PointLight(0xffd6a0,0,p.h?1.6:2.6,2); l.position.copy(W(p.s,p.x,h)); scene.add(l); return l; });
const COR_FITA={ quente:'#ffcf96', neutra:'#fff1de', fria:'#d6e6ff', ambar:'#ffa63d', azul:'#4f9dff' };

"""+s[b:]
rep("plafMat.emissiveIntensity=EST.interna?1.2:0.04; luzesInt.forEach(l=>l.intensity=EST.interna?(EST.noite?2.4:1.4):0);",
"""const kF=EST.dimmer/100; fitaMat.emissive.set(COR_FITA[EST.corFita]); fitaMat.emissiveIntensity=EST.interna?0.4+1.6*kF:0.04;
  luzesInt.forEach((l,i)=>{ l.color.set(COR_FITA[EST.corFita]); l.intensity=EST.interna?(EST.noite?1.6:0.9)*kF*(i===6?0.8:1):0; });""")
rep("const EST={ noite:false,","const EST={ corFita:'quente', dimmer:70, noite:false,")
# ABRE: bancos e porta do banheiro
rep("ABRE.toldo={nome:'Toldo',t:0,alvo:0,apl:setToldo,vel:0.6};","""ABRE.toldo={nome:'Toldo',t:0,alvo:0,apl:setToldo,vel:0.6};
if(portaBanhoPiv) ABRE.banho={nome:'Porta do banheiro',t:0,alvo:0,apl:t=>{ portaBanhoPiv.rotation.y=1.45*t; }};
if(bancosPiv.length){ ABRE.bmot=ABRE.bpas=ABRE.bancos={nome:'Bancos giratórios',t:0,alvo:0,apl:t=>{ bancosPiv.forEach(p=>p.rotation.y=Math.PI*t); }}; }""")
# FP places
rep("  {id:'cama',   nome:'Cama',             s:6.35,x:0.00, eye:1.62,yaw:0,          pitch:-0.08},",
"""  {id:'banho',   nome:'Banheiro',         s:4.20,x:0.45, eye:1.85,yaw:Math.PI/2, pitch:-0.15},
  {id:'cama',    nome:'Cama',             s:6.10,x:0.10, eye:1.55,yaw:0,          pitch:-0.12},""")
rep("function vaiPara(id){ const L=LUGARES.find(l=>l.id===id); Object.assign(FP,{s:L.s,x:L.x,eye:L.eye,yaw:L.yaw,pitch:L.pitch});",
"""function vaiPara(id){ const L=LUGARES.find(l=>l.id===id); Object.assign(FP,{s:L.s,x:L.x,eye:L.eye,yaw:L.yaw,pitch:L.pitch});
  if((id==='mot'||id==='pas')&&ABRE.bancos&&ABRE.bancos.alvo>0.5) FP.yaw=Math.PI;
  if(id==='banho'&&ABRE.banho&&ABRE.banho.alvo<0.5) abre('banho',true);""")
# UI: new buttons
rep('        <button data-abre="toldo">Toldo</button>\n      </div>','        <button data-abre="toldo">Toldo</button>\n        <button data-abre="banho">Porta do banheiro</button>\n        <button data-abre="bancos">Girar bancos</button>\n      </div>')
rep('<div class="row"><button id="noite">Noite</button><button data-luz="interna">Luz interna</button><button data-luz="toldoLuz">Luz do toldo</button></div>',
'''<div class="row"><button id="noite">Noite</button><button data-luz="interna">Fitas de LED internas</button><button data-luz="toldoLuz">Luz do toldo</button></div>
      <div class="row seg" role="group" aria-label="Cor das fitas"><span>Cor</span><button data-cor="quente"><i class="pt" style="background:#ffcf96"></i>Quente</button><button data-cor="neutra"><i class="pt" style="background:#fff1de"></i>Neutra</button><button data-cor="fria"><i class="pt" style="background:#d6e6ff"></i>Fria</button><button data-cor="ambar"><i class="pt" style="background:#ffa63d"></i>Âmbar</button><button data-cor="azul"><i class="pt" style="background:#4f9dff"></i>Azul</button></div>
      <div class="ctl"><label for="dim">Intensidade das fitas <output id="dim-o">70%</output></label><input type="range" id="dim" min="10" max="100" value="70"></div>''')
rep("  ui.querySelectorAll('[data-farol]').forEach(b=>b.setAttribute('aria-pressed',EST.farol===b.dataset.farol));",
"""  ui.querySelectorAll('[data-farol]').forEach(b=>b.setAttribute('aria-pressed',EST.farol===b.dataset.farol));
  ui.querySelectorAll('[data-cor]').forEach(b=>b.setAttribute('aria-pressed',EST.corFita===b.dataset.cor));""")
rep("document.getElementById('noite').addEventListener('click',()=>setNoite(!EST.noite));",
"""document.getElementById('noite').addEventListener('click',()=>setNoite(!EST.noite));
ui.querySelectorAll('[data-cor]').forEach(b=>b.addEventListener('click',()=>{ EST.corFita=b.dataset.cor; if(!EST.interna) EST.interna=true; syncUI(); }));
document.getElementById('dim').addEventListener('input',e=>{ EST.dimmer=+e.target.value; document.getElementById('dim-o').textContent=e.target.value+'%'; if(!EST.interna){EST.interna=true; syncUI();} });""")
rep(".sub2{",".pt{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:5px;vertical-align:-1px;border:1px solid rgba(0,0,0,.25)}\n.sub2{")
rep("carcaça.stl · 7,00 × 2,29 × 2,20 m · v8 de 17/11/2026","carcaça.stl · 7,00 × 2,29 × 2,20 m · v9 de 17/11/2026")
# acabamento note
rep("        <li>Itens de motorhome:","        <li>Interior: forro de ripas de madeira, paredes em feltro, piso vinílico amadeirado, móveis com cantos arredondados e fitas de LED contornando o teto e os rodapés.</li>\n        <li>Itens de motorhome:")
open(p,'w',encoding='utf-8').write(s); print('ok')
