from secoes import *
import numpy as np, json
# winding check: signed volume
V=M.vertices; F=M.faces
vol=np.einsum('ij,ij->i',V[F[:,0]],np.cross(V[F[:,1]],V[F[:,2]])).sum()/6
print('signed volume',vol)
def hit(o,d):
    loc,ri,ti=M.ray.intersects_location([o],[d],multiple_hits=True)
    if len(loc)==0: return None
    dist=np.linalg.norm(loc-np.array(o),axis=1); return loc[np.argmin(dist)]
def canto(s,lado):
    d=np.array([0,0.42,0.91*lado]); d/=np.linalg.norm(d)
    o=[s-3.5,1.70+VAO,0]; p=hit(o,d)
    if p is None: return None
    p=p-d*0.035; return [round(p[0]+3.5,4), round(p[2],4), round(p[1]-VAO,4)]
def teto(s,x):
    p=hit([s-3.5,1.2+VAO,x],[0,1,0]); return None if p is None else p[1]-VAO
def tetoInt(s,x):  # interior ceiling going up from inside
    return teto(s,x)
pts=[]
S=np.round(np.arange(2.02,6.84,0.04),3)
L=[canto(s,1) for s in S]; R=[canto(s,-1) for s in S]
print('L sample',L[::20]); print('R sample',R[::20])
# rear crossing at s=6.86 and front at s=2.0
rear=[]
for x in np.linspace(0.8,-0.8,17):
    h=teto(6.84,x); rear.append([6.84,round(x,4),round(h-0.03,4)])
front=[]
for x in np.linspace(-0.85,0.85,18):
    h=teto(2.0,x); front.append([2.0,round(x,4),round(h-0.03,4)])
print('rear',rear[::4]); print('front',front[::4])
# inner wall at rear for lockers
for s in [6.6,6.7,6.8,6.9]:
    for h in [1.5,1.7,1.85]:
        p=hit([s-3.5,h+VAO,0],[0,0,1]); q=hit([s-3.5-1,h+VAO,0],[1,0,0])
        print('s',s,'h',h,'innerwall x',None if p is None else round(p[2],3), 'rear wall s',None if q is None else round(q[0]+3.5,3))
for s in [6.6,6.75,6.9]: print('teto', s, [round(teto(s,x),3) for x in [0,0.5,0.8]])
json.dump({'L':[p for p in L if p],'R':[p for p in R if p],'tras':rear,'frente':front},open('led.json','w'))
