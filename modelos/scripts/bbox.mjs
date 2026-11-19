import { NodeIO } from '@gltf-transform/core';
import { ALL_EXTENSIONS } from '@gltf-transform/extensions';
import { MeshoptDecoder } from 'meshoptimizer';
import { dequantize, flatten } from '@gltf-transform/functions';
await MeshoptDecoder.ready;
const io = new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({ 'meshopt.decoder': MeshoptDecoder });
const doc = await io.read(process.argv[2]); await doc.transform(dequantize(), flatten());
for (const node of doc.getRoot().listNodes()) { const mesh=node.getMesh(); if(!mesh) continue; const M=node.getWorldMatrix();
 for (const p of mesh.listPrimitives()) { const a=p.getAttribute('POSITION').getArray(), idx=p.getIndices().getArray(); const mn=[1e9,1e9,1e9], mx=[-1e9,-1e9,-1e9];
  for (const i of idx){ const x=a[i*3],y=a[i*3+1],z=a[i*3+2]; const w=[M[0]*x+M[4]*y+M[8]*z+M[12],M[1]*x+M[5]*y+M[9]*z+M[13],M[2]*x+M[6]*y+M[10]*z+M[14]]; for(let k=0;k<3;k++){mn[k]=Math.min(mn[k],w[k]);mx[k]=Math.max(mx[k],w[k]);} }
  console.log(p.getMaterial()?.getName(), idx.length/3, mn.map(v=>v.toFixed(0)).join(','), '|', mx.map(v=>v.toFixed(0)).join(',')); } }
