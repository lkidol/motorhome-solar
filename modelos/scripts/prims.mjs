import { NodeIO } from '@gltf-transform/core';
import { ALL_EXTENSIONS } from '@gltf-transform/extensions';
import { MeshoptDecoder } from 'meshoptimizer';
await MeshoptDecoder.ready;
const io = new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({ 'meshopt.decoder': MeshoptDecoder });
const doc = await io.read(process.argv[2]);
for (const m of doc.getRoot().listMeshes()) for (const p of m.listPrimitives()) {
  const n = p.getIndices() ? p.getIndices().getCount() / 3 : p.getAttribute('POSITION').getCount() / 3;
  const a = p.listSemantics().join(',');
  const pos = p.getAttribute('POSITION'); const mn=[1e9,1e9,1e9], mx=[-1e9,-1e9,-1e9], v=[];
  for (let i=0;i<pos.getCount();i++){ pos.getElement(i,v); for(let k=0;k<3;k++){mn[k]=Math.min(mn[k],v[k]);mx[k]=Math.max(mx[k],v[k]);} }
  console.log(m.getName(), p.getMaterial()?.getName(), Math.round(n), 'verts', pos.getCount(), a, mn.map(x=>x.toFixed(2)).join(','), mx.map(x=>x.toFixed(2)).join(','));
}
