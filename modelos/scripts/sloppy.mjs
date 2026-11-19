// uso: node sloppy.mjs in.glb out.glb maxTrisPorPrimitiva [erroAlvo]
import { NodeIO } from '@gltf-transform/core';
import { ALL_EXTENSIONS } from '@gltf-transform/extensions';
import { MeshoptDecoder, MeshoptSimplifier } from 'meshoptimizer';
import { dequantize, weld, prune, dedup } from '@gltf-transform/functions';
await MeshoptDecoder.ready; await MeshoptSimplifier.ready;
const [,, inp, out, maxT, errS] = process.argv;
const io = new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({ 'meshopt.decoder': MeshoptDecoder });
const doc = await io.read(inp);
await doc.transform(dequantize(), weld());
const max = +maxT, err = +(errS ?? 0.004);
for (const m of doc.getRoot().listMeshes()) for (const p of m.listPrimitives()) {
  const idx = p.getIndices(); if (!idx) continue;
  const n = idx.getCount() / 3; if (n <= max) continue;
  const pos = p.getAttribute('POSITION').getArray();
  const ia = new Uint32Array(idx.getArray());
  // primeiro tenta o simplificador normal sem travar bordas, depois o "sloppy"
  let [res] = MeshoptSimplifier.simplify(ia, pos, 3, max * 3, err, []);
  if (res.length / 3 > max * 1.2) [res] = MeshoptSimplifier.simplifySloppy(ia, pos, 3, null, max * 3, err * 2);
  const Ctor = p.getAttribute('POSITION').getCount() > 65535 ? Uint32Array : Uint16Array;
  idx.setArray(new Ctor(res));
  console.log(p.getMaterial()?.getName(), n, '->', res.length / 3);
}
await doc.transform(prune(), dedup());
for (const e of doc.getRoot().listExtensionsUsed()) if (/meshopt|quantization/i.test(e.extensionName)) e.dispose();
await io.write(out, doc);
