import sys; sys.path.insert(0,'/home/claude/geo')
from load import *; import trimesh
p,i=dec(d['carcaca']); M=trimesh.Trimesh(p.astype(float),i.astype(int),process=False)
VAO=0.19
def hits(orig,dirn):
    loc,ri,ti=M.ray.intersects_location([orig],[dirn],multiple_hits=True)
    return loc
def wall(s,h,lado=1):
    """x of outer side surface at (s,h); ray from outside"""
    L=hits([s-3.5,h+VAO,lado*3],[0,0,-lado])
    if len(L)==0: return None
    return max(L[:,2]) if lado>0 else min(L[:,2])
def frente(x,h):
    L=hits([-6,h+VAO,x],[1,0,0]); return None if len(L)==0 else min(L[:,0])+3.5
def tras(x,h):
    L=hits([6,h+VAO,x],[-1,0,0]); return None if len(L)==0 else max(L[:,0])+3.5
def topo(s,x):
    L=hits([s-3.5,5,x],[0,-1,0]); return None if len(L)==0 else max(L[:,1])-VAO
