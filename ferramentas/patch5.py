import pathlib, re
p = pathlib.Path('/home/claude/motorhome/index.html')
s = p.read_text(encoding='utf-8')

def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)

# 1) imports
rep("import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';",
    "import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';\n"
    "import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';\n"
    "import { MeshoptDecoder } from 'three/addons/libs/meshopt_decoder.module.js';")

# 2) slots para modelos reais (antes de BUILD)
rep("const BUILD={};\nlet portaBanhoPiv=null, bancosPiv=[];",
r"""/* ---------- modelos 3D reais (GLB) ----------
   Peças baixadas de bibliotecas abertas e otimizadas (meshopt). Cada uma entra num "slot" vazio criado pelo
   construtor da peça; o arquivo é carregado depois e encaixado na caixa [s0,s1,x0,x1,h0,h1] do slot.
   rotY gira o modelo antes do encaixe; espelhoZ espelha na lateral; modo 'uniforme' mantém a proporção. */
const MODELOS_PEND=[];
function slotModelo(arq,cfg){ const g=new THREE.Group(); g.name='slot:'+arq; MODELOS_PEND.push({arq,cfg,g}); return g; }
const BUILD={};
let portaBanhoPiv=null, bancosPiv=[];""")

# 3) volante: modelo real + coluna
rep("""  const cen=W((s0+s1)/2,(x0+x1)/2,(h0+h1)/2), ax=new THREE.Vector3(Math.cos(0.55),Math.sin(0.55),0);
  const q=new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0,0,1),ax);
  const aro=new THREE.Mesh(new THREE.TorusGeometry(0.18,0.024,14,48),m); aro.quaternion.copy(q); aro.position.copy(cen); o.push(aro);
  const hub=new THREE.Mesh(new THREE.CylinderGeometry(0.065,0.07,0.06,28),m); hub.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),ax); hub.position.copy(cen); o.push(hub);
  for(const a of [Math.PI/2+0.0, Math.PI*1.17, -Math.PI*0.17]){
    const v=new THREE.Vector3(Math.cos(a)*0.12,Math.sin(a)*0.12,0).applyQuaternion(q);
    const sp=new THREE.Mesh(new RoundedBoxGeometry(0.11,0.022,0.035,2,0.009),m); sp.position.copy(cen).addScaledVector(v,0.52);
    sp.quaternion.copy(q).multiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0,0,1),a)); o.push(sp); }
  const emb=new THREE.Mesh(new THREE.CylinderGeometry(0.025,0.025,0.065,20),al); emb.quaternion.copy(hub.quaternion); emb.position.copy(cen); o.push(emb);
  const fim=W(1.62,(x0+x1)/2,0.93), dir=new THREE.Vector3().subVectors(cen,fim);""",
"""  const cen=W((s0+s1)/2,(x0+x1)/2,(h0+h1)/2), ax=new THREE.Vector3(Math.cos(0.55),Math.sin(0.55),0);
  o.push(slotModelo('volante',{volante:{cen,ax}}));
  const fim=W(1.62,(x0+x1)/2,0.93), dir=new THREE.Vector3().subVectors(cen,fim).multiplyScalar(0.86);""")

# 4) bancos da cabine: base giratória + banco automotivo real
rep("""  o.push(cil((s0+s1)/2,(x0+x1)/2,h0,h0+0.09,0.16,pr), rb(s0+0.05,s1-0.08,x0+0.04,x1-0.04,h0+0.09,h0+0.17,pr,0.03));
  o.push(rb(s0+0.01,s1-0.10,x0+0.05,x1-0.05,h0+0.15,h0+0.26,te,0.05));
  o.push(rb(s0+0.04,s1-0.14,x0+0.15,x1-0.15,h0+0.255,h0+0.27,es,0.006));
  for(const [a,b] of [[x0+0.005,x0+0.085],[x1-0.085,x1-0.005]]) o.push(rb(s0+0.03,s1-0.12,a,b,h0+0.17,h0+0.31,te,0.035));
  const enc=[ rb(s1-0.15,s1-0.02,x0+0.02,x1-0.02,h0+0.27,h0+0.98,te,0.06), rb(s1-0.16,s1-0.145,x0+0.15,x1-0.15,h0+0.36,h0+0.92,es,0.006),
              rb(s1-0.12,s1-0.03,x0+0.005,x0+0.07,h0+0.34,h0+0.90,te,0.03), rb(s1-0.12,s1-0.03,x1-0.07,x1-0.005,h0+0.34,h0+0.90,te,0.03) ];
  for(const e of enc){ e.rotation.z=-0.16; e.position.x+=0.05; o.push(e); }
  const cab=rb(s1-0.11,s1-0.02,x0+0.13,x1-0.13,h0+1.08,h0+1.30,te,0.045); cab.rotation.z=-0.16; cab.position.x+=0.16; o.push(cab);
  for(const dx of [-0.08,0.08]){ const p=cil(s1-0.07,(x0+x1)/2+dx,h0+0.96,h0+1.10,0.007,al); p.rotation.z=-0.16; p.position.x+=0.16; o.push(p); }
  o.push(rb(s0+0.22,s1-0.16,xin-0.035,xin+0.035,h0+0.40,h0+0.46,te,0.025));""",
"""  // base giratória (pedestal + prato) e, em cima, o banco automotivo real (trilhos, regulagens e encosto de cabeça)
  o.push(cil((s0+s1)/2,(x0+x1)/2,h0,h0+0.07,0.17,pr), rb(s0+0.06,s1-0.06,x0+0.05,x1-0.05,h0+0.065,h0+0.10,pr,0.02));
  o.push(slotModelo('banco_cab',{caixa:[s0-0.06,s1+0.02,x0,x1,h0+0.10,h0+1.12],rotY:Math.PI,modo:'uniforme'}));""")

# 5) banheiro: vaso e chuveiro reais
rep("""  o.push(rb(4.30,4.645,0.62,0.985,0.335,0.66,lc,0.06), anel(4.47,0.80,0.68,0.12,0.022,lc), rb(4.33,4.61,0.65,0.95,0.655,0.67,lc,0.007));
  const tampa=rb(4.60,4.635,0.66,0.94,0.70,1.04,lc,0.02); tampa.rotation.z=0.12; o.push(tampa);
""",
"""  o.push(slotModelo('vaso',{caixa:[4.19,4.645,0.58,1.0,0.335,0.80],rotY:-Math.PI/2,modo:'livre',escalaY:1.17,mat:'louca'}));
""")
rep("""  o.push(rb(4.22,4.30,0.985,1.0,1.10,1.18,inx,0.01), cil(4.26,0.97,1.18,1.95,0.007,inx), rb(4.20,4.32,0.90,1.0,1.95,1.965,inx,0.02));""",
"""  // chuveiro na parede da frente, sobre o ralo (s 4,0; x 0,40): barra com ducha manual, misturador e ducha de teto
  o.push(rb(3.80,3.835,0.45,0.55,1.08,1.17,inx,0.012), cil(3.845,0.47,1.11,1.14,0.014,inx), cil(3.845,0.53,1.11,1.14,0.014,inx));
  o.push(slotModelo('chuveiro_barra',{caixa:[3.80,3.97,0.24,0.42,0.95,1.95],modo:'uniforme',mat:'inox'}));
  o.push(slotModelo('chuveiro_ducha',{caixa:[3.80,4.16,0.31,0.49,1.95,2.03],rotY:-Math.PI/2,modo:'uniforme',mat:'inox'}));""")

# 6) banco da sala (frente): base-baú + metade de um banco traseiro automotivo
rep("""  o.push(rb(3.76,4.14,-1.03,-0.47,0.38,0.62,cr,0.02), rb(3.77,4.13,-1.0,-0.52,0.30,0.385,pr,0.01), rb(3.78,4.12,-0.47,-0.462,0.40,0.43,mad,0.004));
  o.push(rb(3.74,3.80,-1.03,-0.45,0.62,1.20,cr,0.02));
  for(const [a,b] of [[-1.02,-0.745],[-0.735,-0.46]]){ o.push(rb(3.84,4.14,a,b,0.62,0.75,es,0.05));
    const bk=rb(3.79,3.88,a+0.01,b-0.01,0.76,1.20,es,0.045); bk.rotation.z=0.10; bk.position.x-=0.01; o.push(bk); }
  const al=rb(3.88,3.98,-1.0,-0.86,0.75,0.95,mo,0.04); al.rotation.z=0.25; al.rotation.y=0.2; o.push(al);""",
"""  o.push(rb(3.76,4.14,-1.03,-0.47,0.38,0.50,cr,0.02), rb(3.77,4.13,-1.0,-0.52,0.30,0.385,pr,0.01), rb(3.78,4.12,-0.47,-0.462,0.40,0.43,mad,0.004));
  o.push(slotModelo('banco_sala',{caixa:[3.73,4.18,-1.03,-0.45,0.44,1.24],modo:'livre',espelhoZ:true}));""")

# 7) banco da sala (trás, sobre a caixa de roda)
rep("""  o.push(rb(4.66,5.0,-1.02,-0.46,0.78,0.88,es,0.045));
  const bk=rb(4.97,5.09,-1.01,-0.47,0.88,1.28,es,0.045); bk.rotation.z=-0.10; o.push(bk);
  o.push(rb(4.55,4.63,-0.98,-0.50,0.47,0.50,mad,0.012));
  const al=rb(4.86,4.96,-0.62,-0.48,0.88,1.08,mo,0.04); al.rotation.z=-0.25; al.rotation.y=-0.2; o.push(al);""",
"""  o.push(rb(4.55,4.63,-0.98,-0.50,0.47,0.50,mad,0.012));
  o.push(slotModelo('banco_sala',{caixa:[4.64,5.10,-1.03,-0.45,0.56,1.30],rotY:Math.PI,modo:'livre'}));""")

# 8) carregamento e encaixe, logo depois do laço dos componentes
rep("""  compObj[c.id]={c,g,mat,mats,edges,center:W((s0+s1)/2,(x0+x1)/2,(h0+h1)/2)};
}
""",
"""  compObj[c.id]={c,g,mat,mats,edges,center:W((s0+s1)/2,(x0+x1)/2,(h0+h1)/2)};
  for(const pm of MODELOS_PEND) if(!pm.comp) pm.comp=c.id;
}
/* posiciona o modelo: gira, mede, escala e centraliza na caixa do slot (fundo apoiado em h0) */
function encaixaModelo(obj,cfg){
  const raiz=new THREE.Group(); raiz.add(obj);
  if(cfg.volante){                                   // eixo do modelo (+Y) vira o eixo da coluna; centro do aro no centro do volante
    const bb=new THREE.Box3().setFromObject(obj), c=bb.getCenter(new THREE.Vector3());
    obj.position.set(-c.x,-(bb.max.y-0.035),-c.z);
    raiz.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),cfg.volante.ax);
    raiz.quaternion.multiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0,1,0),cfg.rolar??Math.PI/2));
    raiz.position.copy(cfg.volante.cen); return raiz;
  }
  obj.rotation.y=cfg.rotY||0; if(cfg.espelhoZ) obj.scale.z=-1;
  obj.updateMatrixWorld(true);
  const bb=new THREE.Box3().setFromObject(obj), tam=bb.getSize(new THREE.Vector3());
  const [s0,s1,x0,x1,h0,h1]=cfg.caixa, alvo=new THREE.Vector3(s1-s0,h1-h0,x1-x0);
  let k=new THREE.Vector3(alvo.x/tam.x,alvo.y/tam.y,alvo.z/tam.z);
  if(cfg.modo==='uniforme'){ const m=Math.min(k.x,k.y,k.z); k.set(m,m,m); }
  if(cfg.escalaY) k.y=Math.min(alvo.y/tam.y,k.x*cfg.escalaY);
  const meio=W((s0+s1)/2,(x0+x1)/2,h0);
  raiz.scale.copy(k);
  raiz.position.set(meio.x-(bb.min.x+bb.max.x)/2*k.x, meio.y-bb.min.y*k.y, meio.z-(bb.min.z+bb.max.z)/2*k.z);
  return raiz;
}
async function bufModelo(arq){ const r=await fetch('modelos/'+arq+'.glb'); if(!r.ok) throw new Error(arq); return r.arrayBuffer(); }
async function carregaModelos(){
  const ldr=new GLTFLoader().setMeshoptDecoder(MeshoptDecoder), cache={};
  const pega=arq=>cache[arq]??=bufModelo(arq).then(b=>ldr.parseAsync(b,''));
  await Promise.all(MODELOS_PEND.map(async pm=>{
    try{
      const gl=await pega(pm.arq), obj=gl.scene.clone(true), o=compObj[pm.comp];
      const subst = pm.cfg.mat ? MI[pm.cfg.mat]() : null;
      obj.traverse(m=>{ if(!m.isMesh) return;
        if(subst){ m.material=subst; }
        else { m.material=m.material.clone(); m.material.envMap=envTex; m.material.envMapIntensity=0.75; }
        m.material.clippingPlanes=[clip]; m.material.side=THREE.FrontSide;
        m.userData.comp=o.c; pickables.push(m); if(!o.mats.includes(m.material)) o.mats.push(m.material); });
      pm.g.add(encaixaModelo(obj,pm.cfg));
    }catch(e){ console.error('modelo',pm.arq,e); }
  }));
  setOpacity(+document.getElementById('op').value);
  if(selId&&compObj[selId]) select(selId,false);
}
""")
rep("carregaMalha().then(()=>preset('p-ext'));","carregaMalha().then(()=>preset('p-ext'));\ncarregaModelos();")
p.write_text(s, encoding='utf-8')
print('ok')
