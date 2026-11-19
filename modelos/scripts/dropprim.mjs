// uso: node dropprim.mjs in.glb out.glb nTris  (remove primitivas com esse número de triângulos)
import { NodeIO } from '@gltf-transform/core';
import { ALL_EXTENSIONS } from '@gltf-transform/extensions';
import { MeshoptDecoder } from 'meshoptimizer';
import { prune } from '@gltf-transform/functions';
await MeshoptDecoder.ready;
const [,, inp, out, nT] = process.argv;
const io = new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({ 'meshopt.decoder': MeshoptDecoder });
const doc = await io.read(inp);
for (const m of doc.getRoot().listMeshes()) for (const p of m.listPrimitives()) if (p.getIndices().getCount()/3 == +nT) { m.removePrimitive(p); p.dispose(); console.log('removida', m.getName()); }
await doc.transform(prune());
for (const e of doc.getRoot().listExtensionsUsed()) if (/meshopt|quantization/i.test(e.extensionName)) e.dispose();
await io.write(out, doc);
