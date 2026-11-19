import sys
p=sys.argv[1]; s=open(p,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    c=s.count(a)
    assert c==n, (c,a[:80])
    s=s.replace(a,b)

# CSS
rep(".note{font-size:12px;color:var(--muted);margin:0}",
""".note{font-size:12px;color:var(--muted);margin:0}
.paints{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:6px}
.paint{display:flex;align-items:center;gap:8px;text-align:left;padding:6px 8px}
.paint .bolinha{width:22px;height:22px;border-radius:50%;flex:none;border:1px solid rgba(0,0,0,.2);position:relative;overflow:hidden}
.paint .bolinha i{position:absolute;left:0;right:0;bottom:0;height:34%;background:#24292d}
.paint .bolinha b{position:absolute;left:0;right:0;bottom:34%;height:12%}
.paint small{display:block;font:11px var(--mono);opacity:.75}
.acab{margin:8px 0 0;padding-left:18px;display:grid;gap:4px;font-size:13px}""")

# header
rep("carcaça.stl · 7,00 × 2,29 × 2,20 m · v5 de 17/11/2026","carcaça.stl · 7,00 × 2,29 × 2,20 m · v6 de 17/11/2026")
rep('<button id="p-geral" aria-pressed="true">Visão geral</button>',
    '<button id="p-ext" aria-pressed="true">Exterior</button>\n    <button id="p-geral">Visão geral</button>')

# paint section in aside (before Camadas)
rep("""    <section>
      <h2>Camadas</h2>""","""    <section>
      <h2>Pintura e acabamento</h2>
      <div class="paints" id="paints" role="group" aria-label="Cor da carroceria"></div>
      <ul class="acab">
        <li>Pintura metálica com verniz; a cor só cobre a carroceria.</li>
        <li>Saia, para-choques e alargadores de para-lama em plástico preto texturizado, até 0,40 m.</li>
        <li>Frisos finos acima da saia.</li>
        <li>Cabine em preto brilhante: colunas A, molduras das janelas e topo. O teto parece flutuar.</li>
        <li>Rodas aro 20″ com tampa aerodinâmica, disco de freio ventilado e pinça na cor do friso.</li>
        <li>Para-lamas internos pretos e carenagem do painel solar em preto.</li>
      </ul>
    </section>
    <section>
      <h2>Camadas</h2>""")

# imports
rep("import { toCreasedNormals } from 'three/addons/utils/BufferGeometryUtils.js';",
"""import { toCreasedNormals } from 'three/addons/utils/BufferGeometryUtils.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';""")

# paint data + material factory after renderer setup lights
rep("const fill = new THREE.DirectionalLight(0xffffff,0.5); fill.position.set(8,4,-6); scene.add(fill);",
r"""const fill = new THREE.DirectionalLight(0xffffff,0.5); fill.position.set(8,4,-6); scene.add(fill);

/* ---------- pintura ----------
   Uma só material para carroceria e portas. A cor de cada ponto sai da posição dele:
   saia preta texturizada (h < 0,40 m e alargadores das rodas), friso fino, cabine em preto brilhante
   (s < 2,62 m e h > 1,12 m) e o resto na cor escolhida, metálica com verniz. */
const PINTURAS = [
  {id:'petroleo', nome:'Azul petróleo', cor:'#1d4e5c', friso:'#e39a2d', pinca:'#e39a2d', tipo:'metálica'},
  {id:'salvia',   nome:'Verde sálvia',  cor:'#8a9e86', friso:'#f1efe6', pinca:'#d8572a', tipo:'sólida'},
  {id:'gelo',     nome:'Branco gelo',   cor:'#e9ece9', friso:'#1f7fa0', pinca:'#1f7fa0', tipo:'perolizada'},
  {id:'areia',    nome:'Areia',         cor:'#c9b48f', friso:'#2c3a2f', pinca:'#b6472b', tipo:'metálica'},
  {id:'laranja',  nome:'Laranja solar', cor:'#d4692a', friso:'#f3f0ea', pinca:'#2a2f33', tipo:'metálica'},
  {id:'grafite',  nome:'Cinza grafite', cor:'#4a5157', friso:'#d9a441', pinca:'#d9a441', tipo:'metálica'},
];
const pmrem = new THREE.PMREMGenerator(renderer);
const envTex = pmrem.fromScene(new RoomEnvironment(renderer), 0.04).texture;
const PINT_U = {
  uBody:{value:new THREE.Color(PINTURAS[0].cor)}, uFriso:{value:new THREE.Color(PINTURAS[0].friso)},
  uClad:{value:new THREE.Color('#23282c')}, uPreto:{value:new THREE.Color('#0d1013')},
  uMetal:{value:0.45},
};
const pinturaMats=[];
function matPintura(){
  const m=new THREE.MeshPhysicalMaterial({color:'#ffffff',roughness:0.32,metalness:0.45,clearcoat:1,clearcoatRoughness:0.06,
    envMap:envTex,envMapIntensity:0.9,side:THREE.DoubleSide,transparent:true,clippingPlanes:[clip]});
  m.onBeforeCompile=sh=>{
    Object.assign(sh.uniforms,PINT_U);
    sh.vertexShader=sh.vertexShader.replace('#include <common>','#include <common>\nvarying vec3 vWP;')
      .replace('#include <project_vertex>','#include <project_vertex>\nvWP=(modelMatrix*vec4(transformed,1.0)).xyz;');
    sh.fragmentShader=sh.fragmentShader.replace('#include <common>',`#include <common>
varying vec3 vWP; uniform vec3 uBody,uFriso,uClad,uPreto; uniform float uMetal;
float zClad,zPreto,zFriso;
float h2(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}`)
      .replace('#include <color_fragment>',`#include <color_fragment>
{ float s=vWP.x+3.5, h=vWP.y-${VAO.toFixed(2)}, ax=abs(vWP.z);
  float da=min(length(vec2(s-1.2,h-0.2)),length(vec2(s-5.2,h-0.2)));
  zClad = (h<0.40 || (da<0.52 && ax>0.80)) ? 1.0 : 0.0;
  zPreto = (zClad<0.5 && s<2.62 && h>1.12) ? 1.0 : 0.0;
  zFriso = (zClad<0.5 && zPreto<0.5 && ((h>0.445&&h<0.465)||(h>0.485&&h<0.495)) && (ax>0.6 || s>6.8)) ? 1.0 : 0.0;
  vec3 c = uBody;
  c = mix(c,uFriso,zFriso);
  c = mix(c,uPreto,zPreto);
  float gr = 0.92+0.16*h2(floor(vWP.xy*420.0)+floor(vWP.zz*420.0));
  c = mix(c,uClad*gr,zClad);
  diffuseColor.rgb = c; }`)
      .replace('#include <roughnessmap_fragment>',`#include <roughnessmap_fragment>
roughnessFactor = zClad>0.5 ? 0.88 : (zPreto>0.5 ? 0.12 : 0.32);`)
      .replace('#include <metalnessmap_fragment>',`#include <metalnessmap_fragment>
metalnessFactor = zClad>0.5 ? 0.0 : (zPreto>0.5 ? 0.2 : (zFriso>0.5 ? 0.6 : uMetal));`)
      .replace('#include <lights_physical_fragment>',`#include <lights_physical_fragment>
material.clearcoat *= (1.0-zClad);`);
  };
  pinturaMats.push(m); return m;
}
const matClad = new THREE.MeshStandardMaterial({color:'#1c2024',roughness:0.9,side:THREE.DoubleSide,transparent:true,clippingPlanes:[clip]});
const matPretoBri = new THREE.MeshPhysicalMaterial({color:'#0d1013',roughness:0.12,metalness:0.2,clearcoat:1,envMap:envTex,envMapIntensity:0.9,side:THREE.DoubleSide,clippingPlanes:[clip]});""")

# shell loading: carcaca with paint, caixas cladding
rep("""      const mat = new THREE.MeshStandardMaterial({color:cor,roughness:vidro?0.1:0.55,metalness:vidro?0.1:0.15,side:THREE.DoubleSide,
        transparent:true,opacity:vidro?0.35:1,depthWrite:!vidro,clippingPlanes:[clip]});""",
"""      const mat = nome==='carcaca' ? matPintura() : nome==='caixas' ? matClad :
        new THREE.MeshPhysicalMaterial({color:'#20303a',roughness:0.04,metalness:0.1,envMap:envTex,envMapIntensity:1.3,side:THREE.DoubleSide,
        transparent:true,opacity:0.55,depthWrite:false,clippingPlanes:[clip]});""")
rep("const lm = new THREE.LineBasicMaterial({color:vidro?'#5f8fb0':'#7d8a94',transparent:true,opacity:0.55,clippingPlanes:[clip]});",
    "const lm = new THREE.LineBasicMaterial({color:vidro?'#0d1013':'#7d8a94',transparent:true,opacity:0.55,clippingPlanes:[clip]});")

# wheels
old_wheels = s[s.index("/* ---------- rodas ---------- */"):s.index("/* ---------- componentes ---------- */")]
new_wheels = r"""/* ---------- rodas ----------
   Pneu 245/45 R20 (Ø0,78 m), roda aro 20″ com tampa aerodinâmica de 5 aberturas, disco ventilado e pinça. */
const pincaMats=[];
{
  const R=RODAS.r, L=RODAS.larg, rAro=0.254;
  // pneu: perfil girado em torno do eixo (ombro arredondado, flanco abaulado)
  const pf=[]; const n=14;
  pf.push(new THREE.Vector2(rAro, -L/2+0.012));
  for(let i=0;i<=n;i++){ const a=-Math.PI/2+Math.PI*i/n; pf.push(new THREE.Vector2(R-0.035+0.035*Math.cos(a)*1.0, (L/2-0.02)*Math.sin(a)*1.0 + 0)); }
  pf.push(new THREE.Vector2(rAro, L/2-0.012));
  const flanco = pf.map((v,i)=> i===0||i===pf.length-1 ? v : v);
  // abaula o flanco: pontos intermediários entre aro e banda
  const perfil=[new THREE.Vector2(rAro,-L/2+0.012), new THREE.Vector2(rAro+0.04,-L/2-0.004), new THREE.Vector2(R-0.06,-L/2-0.006)];
  for(let i=0;i<=n;i++){ const a=-Math.PI/2+Math.PI*i/n; perfil.push(new THREE.Vector2(R-0.04+0.04*Math.cos(a), (L/2-0.006)*Math.sin(a))); }
  perfil.push(new THREE.Vector2(R-0.06,L/2+0.006), new THREE.Vector2(rAro+0.04,L/2+0.004), new THREE.Vector2(rAro,L/2-0.012));
  const pneuG=new THREE.LatheGeometry(perfil,72); pneuG.rotateX(Math.PI/2);
  const pneu = new THREE.MeshStandardMaterial({color:'#1b1e20',roughness:0.92,side:THREE.DoubleSide});
  // face da roda: disco com 5 aberturas
  const face=new THREE.Shape(); face.absarc(0,0,rAro+0.004,0,Math.PI*2);
  for(let k=0;k<5;k++){
    const a0=k*2*Math.PI/5+0.18, a1=a0+2*Math.PI/5-0.36, r0=0.105, r1=0.215;
    const hole=new THREE.Path(); hole.absarc(0,0,r1,a0,a1,false); hole.absarc(0,0,r0,a1,a0,true); face.holes.push(hole);
  }
  const faceG=new THREE.ExtrudeGeometry(face,{depth:0.018,bevelEnabled:true,bevelThickness:0.006,bevelSize:0.004,bevelSegments:2,curveSegments:40});
  const aro=new THREE.MeshPhysicalMaterial({color:'#2e3438',roughness:0.28,metalness:0.8,clearcoat:0.6,envMap:envTex,envMapIntensity:1});
  const aroInt=new THREE.MeshStandardMaterial({color:'#15181a',roughness:0.6,metalness:0.3,side:THREE.DoubleSide});
  const anel=new THREE.MeshPhysicalMaterial({color:'#b9c2c8',roughness:0.18,metalness:1,envMap:envTex,envMapIntensity:1.1});
  const disco=new THREE.MeshStandardMaterial({color:'#7a7f83',roughness:0.45,metalness:0.85,envMap:envTex});
  const pinca=new THREE.MeshPhysicalMaterial({color:PINTURAS[0].pinca,roughness:0.3,metalness:0.1,clearcoat:1,envMap:envTex}); pincaMats.push(pinca);
  for(const s of RODAS.s) for(const sx of [1,-1]){
    const g=new THREE.Group();
    g.add(new THREE.Mesh(pneuG,pneu));
    const barril=new THREE.Mesh(new THREE.CylinderGeometry(rAro,rAro,L-0.02,48,1,true),aroInt); barril.rotation.x=Math.PI/2; g.add(barril);
    const f=new THREE.Mesh(faceG,aro); f.position.z= sx>0 ? L/2-0.03 : -(L/2-0.03); if(sx<0){ f.rotation.y=Math.PI; } g.add(f);
    const lip=new THREE.Mesh(new THREE.TorusGeometry(rAro+0.004,0.007,8,64),anel); lip.position.z=sx*(L/2-0.008); g.add(lip);
    const cubo=new THREE.Mesh(new THREE.CylinderGeometry(0.05,0.055,0.03,32),anel); cubo.rotation.x=Math.PI/2; cubo.position.z=sx*(L/2-0.002); g.add(cubo);
    // disco de freio e pinça visíveis pelas aberturas
    const dg=new THREE.Mesh(new THREE.CylinderGeometry(0.19,0.19,0.03,48),disco); dg.rotation.x=Math.PI/2; dg.position.z=sx*0.02; g.add(dg);
    const pc=new THREE.Mesh(new THREE.BoxGeometry(0.11,0.06,0.05),pinca); pc.position.set(s<3?-0.12:0.12,0.12,sx*0.04); pc.rotation.z= s<3?0.8:-0.8; g.add(pc);
    g.position.copy(W(s,sx*RODAS.x,RODAS.hc));
    layers.rodas.add(g);
  }
}

"""
s=s.replace(old_wheels,new_wheels)

# doors use paint
rep("""  } else if(c.forma==='porta'){
    parts.push(...fazPorta(c,mat));""","""  } else if(c.forma==='porta'){
    parts.push(...fazPorta(c,matPintura()));""")
rep("const mac=new THREE.Mesh(new THREE.BoxGeometry(0.16,0.035,0.03),new THREE.MeshStandardMaterial({color:'#3a4248',metalness:0.5,roughness:0.4,clippingPlanes:[clip]}));",
    "const mac=new THREE.Mesh(new THREE.BoxGeometry(0.16,0.028,0.012),matPretoBri);")
rep("mac.position.copy(W(c.s[1]-0.16,lado*(xw+0.012),1.08)); g.push(mac);",
    "mac.position.copy(W(c.s[1]-0.16,lado*(xw+0.004),1.06)); g.push(mac);")
# glass of doors/windows: darker tinted with reflection
rep("const vidroMat = new THREE.MeshStandardMaterial({color:'#2f526a',roughness:0.08,metalness:0.3,transparent:true,opacity:0.8,side:THREE.DoubleSide,clippingPlanes:[clip]});",
    "const vidroMat = new THREE.MeshPhysicalMaterial({color:'#16232b',roughness:0.04,metalness:0.2,envMap:envTex,envMapIntensity:1.3,transparent:true,opacity:0.85,side:THREE.DoubleSide,clippingPlanes:[clip]});")
rep("const mold=new THREE.MeshStandardMaterial({color:'#2b3338',roughness:0.6,clippingPlanes:[clip]});",
    "const mold=new THREE.MeshPhysicalMaterial({color:'#0d1013',roughness:0.15,clearcoat:1,envMap:envTex,clippingPlanes:[clip]});")

# solar side skin -> gloss black
rep("const skin=new THREE.MeshStandardMaterial({color:GRUPOS.carcaca.cor,roughness:0.55,side:THREE.DoubleSide,clippingPlanes:[clip]});",
    "const skin=matPretoBri;")

# opacity: hide CAD edges at full opacity
rep("lm.opacity=0.25+0.35*(1-a); }","lm.opacity= a>0.98 ? 0.0 : 0.25+0.35*(1-a); lm.visible=lm.opacity>0.01; }")
rep("  for(const mat of portaMats){ mat.userData.op=Math.max(a,0.04); }",
    "  for(const mat of portaMats){ mat.userData.op=Math.max(a,0.04); }\n  matClad.opacity=Math.max(a,0.02); matClad.transparent=a<=0.98; matClad.depthWrite=a>0.98;")

# presets
rep("const presetBtns=['p-geral','p-interior','p-tecnico','p-estac']","const presetBtns=['p-ext','p-geral','p-interior','p-tecnico','p-estac']")
rep("  if(id==='p-geral'){ setOpacity(30); setCut(250); setView('3d'); }",
"""  if(id==='p-ext'){ setOpacity(100); setCut(250); numerosEl.checked=false; setView('3d',new THREE.Vector3(0.2,1.15,0),new THREE.Vector3(-7.9,2.6,-6.4)); }
  else numerosEl.checked=true;
  if(id==='p-geral'){ setOpacity(30); setCut(250); setView('3d'); }""")

# paint picker UI + start in exterior
rep("requestAnimationFrame(loop);\ncarregaMalha();",
r"""requestAnimationFrame(loop);
const paintsEl=document.getElementById('paints');
function setPintura(p){
  PINT_U.uBody.value.set(p.cor); PINT_U.uFriso.value.set(p.friso); PINT_U.uMetal.value = p.tipo==='sólida'?0.05:(p.tipo==='perolizada'?0.25:0.45);
  pincaMats.forEach(m=>m.color.set(p.pinca));
  GRUPOS.carcaca.cor=p.cor; const sw=document.querySelector('#ly-carcaca + .sw'); if(sw) sw.style.background=p.cor;
  paintsEl.querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.p===p.id));
}
for(const p of PINTURAS){
  const b=document.createElement('button'); b.className='paint'; b.dataset.p=p.id;
  b.innerHTML=`<span class="bolinha" style="background:${p.cor}"><b style="background:${p.friso}"></b><i></i></span><span>${p.nome}<small>${p.tipo}</small></span>`;
  b.addEventListener('click',()=>setPintura(p)); paintsEl.appendChild(b);
}
setPintura(PINTURAS[0]);
carregaMalha().then(()=>preset('p-ext'));""")
open(p,'w',encoding='utf-8').write(s)
print("ok")
