import re, subprocess, pathlib, json
src=pathlib.Path('/home/claude/motorhome/index.html').read_text(encoding='utf-8')
lines=src.split('\n')
# module script body
a=src.index('<script type="module">'); b=src.index('</script>',a)
js=src[a+len('<script type="module">'):b]
js=js.replace("from 'three/addons/","from 'three/examples/jsm/")
js=js.replace("const r = await fetch('malha.json'); const d = await r.json();","const d = DADO('malha');")
js=js.replace("['detalhes.json','relevos.json'].map(async f=>{ try{ return await (await fetch(f)).json(); }catch(e){ console.error(f,e); return []; } })",
              "['detalhes','relevos'].map(async f=>{ try{ return DADO(f); }catch(e){ console.error(f,e); return []; } })")
js=js.replace("async function bufModelo(arq){ const r=await fetch('modelos/'+arq+'.glb'); if(!r.ok) throw new Error(arq); return r.arrayBuffer(); }",
  "async function bufModelo(arq){ const t=document.getElementById('m-'+arq).textContent.trim(); const bin=atob(t); const u=new Uint8Array(bin.length); for(let i=0;i<bin.length;i++) u[i]=bin.charCodeAt(i); return u.buffer; }")
assert 'fetch(' not in js
import os
if os.environ.get('TESTE'): js+='\n'+pathlib.Path('/home/claude/bundle/debug.js').read_text()
js="const DADO=id=>JSON.parse(document.getElementById('d-'+id).textContent);\n"+js
pathlib.Path('main.js').write_text(js,encoding='utf-8')
subprocess.run(['node_modules/.bin/esbuild','main.js','--bundle','--minify','--format=esm','--target=es2020','--outfile=bundle.js'],check=True)
bun=pathlib.Path('bundle.js').read_text(encoding='utf-8')
assert '</script' not in bun.lower()
# html head/body without importmap, module and google fonts
im0=src.index('<script type="importmap">'); im1=src.index('</script>',im0)+len('</script>')
html=src[:im0]+src[im1:a]
html=re.sub(r'<link rel="preconnect"[^>]*>\n?','',html); html=re.sub(r'<link href="https://fonts.googleapis.com[^>]*>\n?','',html)
dados=''
for k,f in [('malha','malha.json'),('detalhes','detalhes.json'),('relevos','relevos.json')]:
    t=pathlib.Path('/home/claude/motorhome/'+f).read_text(encoding='utf-8'); json.loads(t)
    dados+=f'<script type="application/json" id="d-{k}">{t}</script>\n'
import base64
for f in sorted(pathlib.Path('/home/claude/motorhome/modelos').glob('*.glb')):
    dados+=f'<script type="application/octet-stream" id="m-{f.stem}">'+base64.b64encode(f.read_bytes()).decode()+'</script>\n'
out=html+dados+'<script type="module">\n'+bun+'\n</script>\n'+src[b+len('</script>'):]
pathlib.Path(('/home/claude/motorhome/teste_3d.html' if os.environ.get('TESTE') else '/home/claude/motorhome/motorhome_solar_3d.html')).write_text(out,encoding='utf-8')
print(len(out)/1e6,'MB')
