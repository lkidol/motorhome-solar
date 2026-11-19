window.__cam=(t,c)=>{ controls.target.copy(W(...t)); camera.position.copy(W(...c)); anim=null; camera.fov=50; camera.updateProjectionMatrix(); };
window.__check=()=>{ const shell=[]; layers.carcaca.traverse(o=>{ if(o.isMesh) shell.push(o); }); const rc=new THREE.Raycaster(); const out={};
  const S=new Set(['interior','cabine']);
  for(const [id,o] of Object.entries(compObj)){ if(!S.has(o.c.grupo)) continue; const v=new THREE.Vector3(); let nFora=0,nRoda=0,n=0; const ex=[];
    o.g.updateMatrixWorld(true);
    o.g.traverse(m=>{ if(!m.isMesh) return; const pa=m.geometry.attributes.position; const step=Math.max(1,Math.floor(pa.count/400));
      for(let i=0;i<pa.count;i+=step){ v.fromBufferAttribute(pa,i).applyMatrix4(m.matrixWorld); n++;
        const s=v.x+3.5,h=v.y-VAO,x=v.z; let bad=false;
        if(Math.abs(x)>0.575 && h<0.70 && (Math.abs(s-1.2)<0.52||Math.abs(s-5.2)<0.52)){ nRoda++; bad=true; }
        if(s>0.45&&s<6.95&&Math.abs(x)>wallX(s)-0.025){ nFora++; bad=true; }
        if(s>1.6&&s<6.9&&h>roofH(s)-0.025){ nFora++; bad=true; }
        if(bad&&ex.length<3) ex.push([+s.toFixed(3),+x.toFixed(3),+h.toFixed(3)]);
      } });
    if(nFora||nRoda) out[id]={n,nFora,nRoda,ex}; }
  return out; };
window.__dbg=id=>{ const o=compObj[id]; const r=[]; o.g.updateMatrixWorld(true); o.g.traverse(m=>{ if(!m.isMesh) return; const b=new THREE.Box3().setFromObject(m); r.push([m.material.name||m.material.type, (m.material.clippingPlanes||[]).length, +(b.min.y-VAO).toFixed(3), +(b.max.y-VAO).toFixed(3), +(b.min.x+3.5).toFixed(3), +(b.max.x+3.5).toFixed(3)]); }); return r; };
window.__ray=(s,x,h0)=>{ const rc=new THREE.Raycaster(W(s,x,h0),new THREE.Vector3(0,-1,0)); const objs=[]; scene.traverse(o=>{ if(o.isMesh&&o.visible) objs.push(o); }); return rc.intersectObjects(objs,false).slice(0,4).map(i=>[+(i.point.y-VAO).toFixed(3), i.object.material.name||i.object.material.type]); };
