from secoes import *
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
S=np.arange(-0.02,7.03,0.01); H=np.arange(-0.02,2.42,0.01)
O=[];D=[]
for h in H:
    for s in S: O.append([s-3.5,h+VAO,3]); D.append([0,0,-1])
loc,ri,ti=M.ray.intersects_location(np.array(O),np.array(D),multiple_hits=False)
img=np.full(len(O),np.nan); img[ri]=loc[:,2]
img=img.reshape(len(H),len(S)); np.save('lado.npy',img)
fig,ax=plt.subplots(figsize=(18,6.5)); im=ax.imshow(img,origin='lower',extent=[S[0],S[-1],H[0],H[-1]],cmap='viridis',vmin=0.8,vmax=1.15)
ax.set_xticks(np.arange(0,7.01,0.25)); ax.set_yticks(np.arange(0,2.41,0.1)); ax.grid(alpha=.3); plt.colorbar(im)
for s in [1.2,5.2]: ax.add_patch(plt.Circle((s,0.2),0.39,fill=False,color='r'))
plt.tight_layout(); plt.savefig('lado.png',dpi=70)
