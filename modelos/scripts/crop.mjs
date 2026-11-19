// uso: node crop.mjs in.glb out.glb xmin xmax ymin ymax zmin zmax  (mantém triângulos com centróide dentro da caixa, em coordenadas do mundo)
import { NodeIO } from '@gltf-transform/core';
import { ALL_EXTENSIONS } from '@gltf-transform/extensions';
import { MeshoptDecoder } from 'meshoptimizer';
import { dequantize, prune, flatten, unweld, weld } from '@gltf-transform/functions';
await MeshoptDecoder.ready;
const [,, inp, out, ...b] = process.argv; const B = b.map(Number);
const io = new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({ 'meshopt.decoder': MeshoptDecoder });
const doc = await io.read(inp);
await doc.transform(dequantize(), flatten());
// aplica a matriz do nó nas posições, para cortar em coordenadas do mundo
for (const node of doc.getRoot().listNodes()) {
  const mesh = node.getMesh(); if (!mesh) continue;
  const M = node.getWorldMatrix();
  for (const p of mesh.listPrimitives()) {
    const pos = p.getAttribute('POSITION'); const a = pos.getArray(); const w = new Float32Array(a.length);
    for (let i = 0; i < a.length; i += 3) { const x=a[i],y=a[i+1],z=a[i+2];
      w[i]=M[0]*x+M[4]*y+M[8]*z+M[12]; w[i+1]=M[1]*x+M[5]*y+M[9]*z+M[13]; w[i+2]=M[2]*x+M[6]*y+M[10]*z+M[14]; }
    const idx = p.getIndices().getArray(); const keep = [];
    for (let t = 0; t < idx.length; t += 3) {
      let ok=true; for (let k=0;k<3;k++){ const j=idx[t+k]*3; const cx=w[j],cy=w[j+1],cz=w[j+2];
        if (!(cx>=B[0]&&cx<=B[1]&&cy>=B[2]&&cy<=B[3]&&cz>=B[4]&&cz<=B[5])) ok=false; }
      if (ok) keep.push(idx[t],idx[t+1],idx[t+2]);
    }
    pos.setArray(w); p.getIndices().setArray(new Uint32Array(keep));
    console.log(p.getMaterial()?.getName(), idx.length/3, '->', keep.length/3);
  }
  node.setMatrix([1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]);
}
await doc.transform(unweld(), weld(), prune());
for (const e of doc.getRoot().listExtensionsUsed()) if (/meshopt|quantization/i.test(e.extensionName)) e.dispose();
await io.write(out, doc);
