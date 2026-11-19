import sys; sys.path.insert(0,'/home/claude/geo')
from load import *
import numpy as np, trimesh, json
VAO=0.19
res={}
for nome in ['carcaca','caixas','vidro']:
    p,i=dec(d[nome]); M=trimesh.Trimesh(p.astype(float),i.astype(int),process=False)
    A=M.area_faces; N=M.face_normals; C=M.triangles_center
    s=C[:,0]+3.5; h=C[:,1]-VAO; x=C[:,2]
    cc=np.c_[np.clip(C[:,0],-1.6,2.9), np.full(len(C),1.30), np.zeros(len(C))]
    dentro=np.einsum('ij,ij->i',N,cc-C)>0
    out={'area_total':A.sum(),'vol':float(M.volume) if M.is_watertight else None,'watertight':bool(M.is_watertight)}
    if nome=='carcaca':
        ext=~dentro
        reg={}
        def r(mask): return float(A[mask].sum())
        reg['teto']=r(ext&(N[:,1]>0.5)); reg['fundo']=r(ext&(N[:,1]<-0.5))
        reg['laterais']=r(ext&(np.abs(N[:,2])>=0.5)&(np.abs(N[:,1])<=0.5))
        reg['frente']=r(ext&(N[:,0]<-0.5)&(np.abs(N[:,1])<=0.5)&(np.abs(N[:,2])<0.5))
        reg['traseira']=r(ext&(N[:,0]>0.5)&(np.abs(N[:,1])<=0.5)&(np.abs(N[:,2])<0.5))
        out['externa']=float(A[ext].sum()); out['interna']=float(A[dentro].sum()); out['regioes']=reg
        # centroid of external skin
        out['cg_ext']=[float((s*A)[ext].sum()/A[ext].sum()), float((x*A)[ext].sum()/A[ext].sum()), float((h*A)[ext].sum()/A[ext].sum())]
        # signed volume
        V=M.vertices; F=M.faces
        out['vol_signed']=float(np.einsum('ij,ij->i',V[F[:,0]],np.cross(V[F[:,1]],V[F[:,2]])).sum()/6)
        # inertia props of outer skin as thin shell
    else:
        out['cg']=[float((s*A).sum()/A.sum()), float((x*A).sum()/A.sum()), float((h*A).sum()/A.sum())]
    out['bounds']=[[float(v) for v in M.bounds[0]],[float(v) for v in M.bounds[1]]]
    res[nome]=out
json.dump(res,open('casca.json','w'),indent=1); print(json.dumps(res,indent=1))
