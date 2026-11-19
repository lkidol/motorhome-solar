import json, numpy as np
D=json.load(open('massa.json')); g=9.81
itens=D['itens']+D['var']
nao_susp=lambda i: i['sub']=='Rodas e suspensão' and ('Roda + pneu' in i['nome'] or 'Cubo' in i['nome'])
s=np.linspace(0,7,701); ds=s[1]-s[0]
q=np.zeros_like(s)  # kg/m sprung
for i in itens:
    if nao_susp(i): continue
    m=i['m']*(0.5 if 'Suspensão' in i['nome'] else 1)
    a,b=max(0,i['s']-i['ds']/2),min(7,i['s']+i['ds']/2)
    mask=(s>=a)&(s<=b)
    if mask.sum()==0: mask=np.abs(s-i['s'])==np.abs(s-i['s']).min()
    q[mask]+=m/(mask.sum()*ds)
Msus=q.sum()*ds
w=q*g  # N/m
# reactions at 1.2 and 5.2
Fz=w.sum()*ds; Mz=(w*s).sum()*ds
Rr=(Mz-Fz*1.2)/4.0; Rf=Fz-Rr
V=np.cumsum(w)*ds; V=-V+Rf*(s>=1.2)+Rr*(s>=5.2)
M=np.cumsum(V)*ds
iM=np.argmax(np.abs(M)); Mmax=M[iM]
Msag=M.max(); Mhog=M.min()
# section
b,h,t=0.08,0.25,0.006
I=(b*h**3-(b-2*t)*(h-2*t)**3)/12; Wz=I/(h/2)
sig1=max(abs(Msag),abs(Mhog))/(2*Wz)/1e6
E=69e9
# deflection by double integration of M/EI (2 rails), supports zero at axles
k=M/(E*2*I); th=np.cumsum(k)*ds; y=np.cumsum(th)*ds
i1,i2=np.argmin(abs(s-1.2)),np.argmin(abs(s-5.2))
# remove rigid body so y(1.2)=y(5.2)=0
A=np.array([[1,s[i1]],[1,s[i2]]]); c=np.linalg.solve(A,[y[i1],y[i2]]); y=y-(c[0]+c[1]*s)
mid=y[(s>1.2)&(s<5.2)]; flecha=abs(mid).max()*1000
estac=np.arange(0,7.0,0.5)
dist=[float(q[(s>=a)&(s<a+0.5)].sum()*ds) for a in estac]
res=dict(Msus=Msus,Rf=Rf/g,Rr=Rr/g,Msag=Msag,Mhog=Mhog,s_Msag=float(s[np.argmax(M)]),s_Mhog=float(s[np.argmin(M)]),I=I,W=Wz,sig1=sig1,sig25=sig1*2.5,flecha_mm=flecha,
         dist=[dict(est=f'{a:.1f}–{a+0.5:.1f}',kg=round(m,1)) for a,m in zip(estac,dist)])
m=D['cen']['proj']['m']; hc=D['cen']['proj']['hsolo']; L=4.0; tr=1.70
res['frenagem_dF']=m*0.8*g*hc/L/g; res['lateral_dF']=m*0.6*g*hc/tr/g
res['bat_long']=860*20*g/1e3; res['bat_lat']=860*8*g/1e3
# drawers
md=4.42*6.5; lev=(1.03-0.65+1.4)-1.04
res['gaveta_Mest']=md*g*lev; q_=0.5*1.18*20**2*1.3; res['gaveta_vento_F']=q_*4.42; res['gaveta_vento_M']=q_*4.42*lev
# sandwich D
E1,t1,E2,t2,dd=70e9,0.003,9e9,0.003,0.027
res['D_sand']=E1*t1*E2*t2*dd**2/(E1*t1+E2*t2)
json.dump(res,open('estrut.json','w'),indent=1)
for k,v in res.items(): print(k, v if k=='dist' else round(v,4) if isinstance(v,float) else v)
