import re, json, math, pathlib, numpy as np
AQUI=pathlib.Path(__file__).resolve().parent
html=(AQUI.parent/'site'/'configurador.html').read_text(encoding='utf-8')
F=json.loads(re.search(r'const FUROS = (\{.*?\});\n',html).group(1))
C=json.load(open(AQUI/'casca.json'))
def area_poly(P):
    P=np.array(P); x,y=P[:,0],P[:,1]; return abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))/2
def vidro_porta(P,vh,folga=0.07):
    hmax=max(p[1] for p in P); pts=[p for p in P if vh<=p[1]<=hmax-folga]; k=len(pts)//2
    jan=[[s+folga,h] for s,h in pts[:k]]+[[s-folga,h] for s,h in pts[k:]]
    return area_poly(jan)
A_portaE=area_poly(F['frenteE']); A_portaD=area_poly(F['frenteD']); A_casa=area_poly(F['casa'])
Av_E=vidro_porta(F['frenteE'],1.16); Av_D=vidro_porta(F['frenteD'],1.16); Av_casa=vidro_porta(F['casa'],1.40)
A_jan=sum(area_poly(P) for P in F['janela'])
geo=dict(A_portaE=A_portaE,A_portaD=A_portaD,A_casa=A_casa,Av_E=Av_E,Av_D=Av_D,Av_casa=Av_casa,A_jan=A_jan)
# ---------- sandwich ----------
rhoAl=2700
camadas=[('Pele externa Al 5754-H22',3.0,2700),('Adesivo PU estrutural',0.5,1200),('Núcleo PIR',23.0,35),('Adesivo PU estrutural',0.5,1200),('Compensado de choupo',3.0,480)]
kgm2=sum(t/1000*r for _,t,r in camadas); esp=sum(t for _,t,_ in camadas)
A_ext=C['carcaca']['externa']; reg=C['carcaca']['regioes']
cgS=C['carcaca']['cg_ext']
itens=[]  # (sub, nome, material, massa, s, x, h, dims para inércia (ds,dx,dh))
def add(sub,nome,mat,m,s,x,h,ds=0.2,dx=0.2,dh=0.2,cen='vazio'):
    itens.append(dict(sub=sub,nome=nome,mat=mat,m=m,s=s,x=x,h=h,ds=ds,dx=dx,dh=dh,cen=cen))
# Carroceria
add('Carroceria','Casca sanduíche 30 mm (sem portas)',f'Al 3 mm + PIR 23 mm + compensado 3 mm ({kgm2:.2f} kg/m²)',A_ext*kgm2,*cgS,6.5,2.0,2.0)
add('Carroceria','Quadro de perfis (cavernas e longitudinais)','Al 6063-T6, tubo 40×40×2 mm (0,82 kg/m), ~165 m',165*0.821*1.10,3.6,0,1.15,6.5,2.2,2.1)
add('Carroceria','Caixas de roda (4)',f'Mesmo sanduíche da carroceria: Al 5754 3 mm + PIR 23 mm + choupo 3 mm ({kgm2:.2f} kg/m²)',C['caixas']['area_total']*kgm2,3.2,0,0.40,4.4,1.8,0.6)
add('Carroceria','Adesivos, selantes e rebites de montagem','PU/MS polímero',18,3.5,0,1.1,6,2,2)
# Aberturas
for nome,A,Av,s,x,hg,ferr in [('Porta do motorista',A_portaE,Av_E,2.15,1.08,1.1,9),('Porta do passageiro',A_portaD,Av_D,2.15,-1.08,1.1,9),('Porta de entrada',A_casa,Av_casa,3.20,-1.07,1.15,12)]:
    add('Aberturas',nome,'Sanduíche 30 mm + vidro temperado 4 mm + dobradiças/fechadura',(A-Av)*kgm2+Av*10.0+ferr,s,x,hg,0.8,0.08,1.8)
add('Aberturas','Para-brisa laminado 5 mm (3,25 m²)','Vidro laminado (2×2,1 mm + PVB 0,76 mm)',3.25*12.5,0.97,0,1.64,1.3,2.0,0.9)
add('Aberturas','Janela da sala (2 folhas)','Acrílico duplo PMMA 2×3 mm + caixilho',A_jan*7.5+4,4.30,-1.06,1.40,1.0,0.06,1.0)
# Chassi
long=2*6.6*(0.25*0.08-0.238*0.068)*rhoAl
trav=8*1.9*(0.10*0.05-0.092*0.042)*rhoAl
add('Chassi','Longarinas (2)','Al 6061-T6, tubo 250×80×6 mm, 6,6 m',long,3.55,0,0.125,6.6,1.5,0.25)
add('Chassi','Travessas (8)','Al 6061-T6, tubo 100×50×4 mm, 1,9 m',trav,3.4,0,0.06,5.5,1.9,0.1)
add('Chassi','Subchassi dianteiro (torres, direção)','Aço S355 soldado',60,1.2,0,0.25,0.8,1.6,0.5)
add('Chassi','Subchassi traseiro (motor, suspensão)','Aço S355 soldado',55,5.2,0,0.25,0.8,1.6,0.5)
add('Chassi','Berço e chapa de proteção da bateria','Al 5083 5 mm + quadro 6061',47,2.8,0,0.02,1.7,1.4,0.1)
add('Chassi','Barras de impacto e reboque, suportes','Aço/Al',25,3.5,0,0.2,7,2,0.3)
add('Chassi','Piso elevado estrutural','Painel colmeia Al 20 mm (5 kg/m²) + apoios',6.5*5.0+10,3.2,0,0.29,2.9,2.08,0.02)
# Rodas e suspensão
for s in (1.2,5.2):
    for x in (0.85,-0.85):
        add('Rodas e suspensão','Roda + pneu 245/70 R17.5','Aço 17,5×6,75 + pneu radial LT',48,s,x,0.20,0.79,0.24,0.79)
        add('Rodas e suspensão','Cubo, disco ventilado e pinça','Disco ref. Iveco Daily 70C15 Ø 306 × 28 mm (ferro fundido EN-GJL-250) + aço',16,s,x*0.9,0.20,0.35,0.15,0.35)
add('Rodas e suspensão','Suspensão dianteira (braços, molas, amortecedores)','Aço',90,1.2,0,0.25,0.5,1.6,0.5)
add('Rodas e suspensão','Suspensão traseira independente','Aço',100,5.2,0,0.25,0.5,1.6,0.5)
add('Rodas e suspensão','Direção elétrica + coluna','Aço/Al',25,1.0,0.3,0.3,0.5,0.6,0.5)
add('Rodas e suspensão','Estepe (roda + pneu)','Aço + borracha',48,6.05,-0.45,0.665,0.79,0.79,0.22)
# Trem de força e elétrico
# bateria NCM de 203,6 kWh (itens 10, 34 e 35): 764 células equivalentes à LG E65D (0,906 kg) em 2 camadas sobre placas frias
add('Elétrico e tração','Células da bateria de tração (764, NCM, 203,6 kWh)','Pouch equivalente à LG E65D, 0,906 kg cada',764*0.906,2.8,0,0.16,1.56,1.25,0.23)
add('Elétrico e tração','Caixa do pack AT, BMS e barramentos','Estrutura do pack (Inventário de Massas, aba Elétrica)',200,2.8,0,0.16,1.6,1.3,0.26)
add('Elétrico e tração','Placas frias da bateria (2)','Al, 1250 × 1560 × 6 mm, 120 canais de 10 × 3 mm',2*19.4,2.8,0,0.10,1.56,1.25,0.12)
add('Elétrico e tração','Gap filler sob as células','DOWSIL TC-5515 LT, 1,5 mm',9,2.8,0,0.10,1.56,1.25,0.12)
add('Elétrico e tração','Motor de tração Cascadia SS-320-180','Aço/Al/cobre (massa do Inventário de Massas)',149,5.1,0,0.415,0.5,0.5,0.5)
add('Elétrico e tração','Redutor 8:1 com diferencial (hipótese)','Carcaça de Al + engrenagens de aço, 450 × 350 × 300 mm',60,5.1,0,0.30,0.45,0.35,0.30)
add('Elétrico e tração','Semieixos (2)','Aço forjado',18,5.2,0,0.25,0.2,1.4,0.1)
add('Elétrico e tração','Inversor de tração Cascadia CM350SiC','Al fundido + eletrônica (Inventário de Massas)',15,5.65,0,0.40,0.3,0.4,0.15)
add('Elétrico e tração','Caixa de alta tensão + chave de serviço','Aço/cobre',15,3.8,0.55,0.15,0.3,0.4,0.2)
add('Elétrico e tração','Baía técnica (carregador 11 kW, DC-DC, conversor solar BrightLoop DCHV, inversor 3 kVA)','Eletrônica',40,6.03,0.48,0.65,0.65,0.85,0.26)
add('Elétrico e tração','Bateria auxiliar 12 V LFP 200 Ah','LFP',22,6.2,0.7,0.6,0.35,0.2,0.25)
add('Elétrico e tração','Chicotes AT e BT (fases: Coroplast 9-2611, 70 mm²)','Cobre + isolação',60,3.5,0,0.3,6,1.5,0.5)
# arrefecimento (itens 10, 34 e 35): um circuito para motor, inversor, conversor solar e bateria, sem chiller
add('Água e térmico','Radiador sob medida (núcleo 800 × 400 × 66 mm)','Al brasado, fluxo cruzado em 4 passes',8,0.19,0,0.545,0.07,0.88,0.42)
add('Água e térmico','Ventiladores SPAL VA18 de 16″ (2)','Aspirantes, 12 V',2*2.57,0.28,0,0.545,0.1,0.8,0.4)
add('Água e térmico','Bombas Pierburg CWA 150 e Rheinmetall CWP 50 + válvula de 3 vias','12 V',1.0+0.6+0.4,0.45,0,0.40,0.2,0.3,0.2)
add('Água e térmico','Fluido de arrefecimento 19,8 L','Etilenoglicol 50 % em água',21,2.9,0,0.25,5,1,0.3)
add('Água e térmico','Mangueiras (4 m de Ø 25 e 12 m de Ø 16) + reservatório de 1 L','EPDM',4.8+0.5,2.9,0,0.25,5,1,0.3)
# lubrificação (item 12)
add('Elétrico e tração','Óleos do motor (ATF 4,6 L) e do redutor (2,5 L) + bomba auxiliar','Dexron-VI ATF + Mobilube 1 SHC 75W-90',3.8+2.2+1.0,5.1,0,0.30,0.5,0.5,0.3)
# Água e térmico
add('Água e térmico','Tanque de água limpa 100 L (vazio)','PEAD rotomoldado',10,4.23,-0.55,0.16,0.5,0.9,0.24)
add('Água e térmico','Tanque de água cinza 80 L (vazio)','PEAD',8,4.23,0.48,0.16,0.5,0.75,0.24)
add('Água e térmico','Boiler 10 L + bomba (vazio)','Inox + Al',10,2.98,0.81,0.54,0.4,0.38,0.42)
# climatização (itens 11 e 32): 2 FreshWell sob o painel, MaxxFan no teto traseiro
add('Água e térmico','Ar-condicionado Dometic FreshWell 3000 (2)','2,7 kW de frio e 3,0 kW de calor cada, 230 V',2*21,0.634,0,0.183,0.628,0.82,0.286)
add('Água e térmico','Exaustor MaxxFan Deluxe','12 V, 30 W',5.4,6.58,0,2.06,0.42,0.59,0.13)
add('Água e térmico','Tubulação, registros, ralos','PEX/PP',8,3.8,0,0.2,3,1.6,0.2)
# Interior
add('Interior','Piso: vinílico 2 mm + tapete','PVC vinílico (3,4 kg/m²)',7.0*3.4+2,3.2,0,0.30,2.9,2.08,0.01)
add('Interior','Forro do teto em ripas','Madeira 6 mm (3,0 kg/m²)',12.9*0.85*3.0,4.0,0,2.15,4.8,1.9,0.01)
add('Interior','Revestimento das paredes','Feltro automotivo 4 mm (0,6 kg/m²)',22*0.6,3.8,0,1.3,5,2,1.5)
add('Interior','Painel de instrumentos + telas + console','PP/ABS + aço + eletrônica',45,1.25,0,0.82,1.1,1.9,0.4)
add('Interior','Bancos da cabine giratórios (2)','Aço + espuma PU + tecido',64,2.34,0,0.75,0.6,1.6,1.0)
add('Interior','Volante, pedais, colunas','Aço/Al/PU',10,1.85,0.55,0.8,0.4,0.4,0.7)
add('Interior','Cozinha (gabinete, bancada, pia, cooktop Dometic CVI1525)','Choupo 15 mm + carvalho 35 mm + inox',48,2.99,0.74,0.75,0.5,0.58,0.9)
add('Interior','Geladeira Dometic RC 10.4M90 (90 L, 12 V)','Aço + PU',21,3.49,0.74,0.75,0.5,0.55,0.8)
add('Interior','Armário aéreo da cozinha','Choupo 12 mm',16,3.24,0.84,1.845,1.0,0.32,0.45)
add('Interior','Banheiro (paredes GRP, piso de box, porta)','GRP 4 mm + choupo',42,4.23,0.58,1.2,0.9,0.89,1.78)
add('Interior','Vaso cassete + cuba + armário com espelho + chuveiro','ABS/cerâmica/inox',30,4.23,0.8,0.9,0.8,0.4,1.2)
add('Interior','Banco da sala (frente) com baú','Choupo 15 mm + espuma D33',22,3.94,-0.74,0.7,0.4,0.58,0.9)
add('Interior','Mesa (tampo carvalho + coluna inox)','Carvalho 30 mm + inox',14,4.39,-0.71,0.8,0.46,0.58,0.7)
add('Interior','Banco da sala (trás) sobre a caixa de roda','Choupo 15 mm + espuma',22,4.87,-0.74,0.9,0.46,0.58,0.9)
add('Interior','Guarda-roupa','Choupo 12 mm',22,4.96,0.81,1.4,0.48,0.45,1.33)
add('Interior','Degraus e tampa do motor','Choupo 18 mm + carvalho',14,4.9,0,0.45,0.6,0.9,0.6)
add('Interior','Estrado da cama + frente','Choupo 18 mm',26,5.91,0,0.75,1.42,1.91,0.1)
add('Interior','Colchão 1,4 × 1,9 m + roupa de cama','Espuma D28 140 mm + têxteis',22,5.9,0,0.88,1.4,1.9,0.15)
add('Interior','Armários sobre o pé da cama (3 portas)','Choupo 12 mm',14,6.77,0,1.68,0.31,1.6,0.36)
add('Interior','Fechamentos, soleiras e forros das caixas de roda','Choupo/ABS + Al',22,3.0,0,0.35,4.6,2.1,0.4)
add('Interior','Fitas de LED, luminárias e fiação interna','Al + cobre',8,4.0,0,2.0,5,2,0.2)
add('Interior','Cortinas e persianas das janelas','Têxtil/plissado',8,3.0,0,1.5,3,2,0.5)
# Solar e acessórios
add('Solar e externos','Painel solar fixo 8,8 m² (rodando)','Módulos leves sem vidro 3,5 kg/m² + suporte Al 2 kg/m²',8.8*5.5,4.1,0,2.22,4.4,2.0,0.06)
add('Solar e externos','Gavetas solares 2 × 4,4 m² + trilhos e atuadores','Módulos leves + quadro Al + trilhos',2*(4.42*6.5)+30,3.9,0,2.23,3.4,2.6,0.05)
add('Solar e externos','Carenagem lateral do teto','Al 1,5 mm',10,4.1,0,2.25,4.4,2.08,0.08)
add('Solar e externos','Toldo em cassete 3,1 m','Al anodizado + lona acrílica',26,4.35,-1.13,2.10,3.15,0.12,0.1)
add('Solar e externos','Degrau elétrico','Al + motor 12 V',15,3.2,-1.0,-0.02,0.5,0.5,0.05)
add('Solar e externos','Para-choques, alargadores, soleiras, saias, difusor, aerofólio','PP-EPDM (TPO) 3 mm + suportes',60,3.6,0,0.35,7,2.3,0.6)
add('Solar e externos','Faróis, lanternas, retrovisores câmera, limpadores','PC/PMMA + eletrônica',16,2.5,0,1.0,6,2,0.8)
# --------- cenários: cargas variáveis ----------
var=[]
def v(nome,m,s,x,h,cen): var.append(dict(sub='Variáveis',nome=nome,mat='—',m=m,s=s,x=x,h=h,ds=0.3,dx=0.3,dh=0.3,cen=cen))
v('Motorista',75,2.34,0.55,0.95,'om'); v('Água limpa 20 L',20,4.23,-0.55,0.1,'om')
v('Passageiro',75,2.34,-0.55,0.95,'proj')
v('Água limpa +80 L (tanque cheio)',80,4.23,-0.55,0.16,'proj'); v('Boiler cheio 10 L',10,2.98,0.81,0.54,'proj')
v('Água cinza 50 % (40 L)',40,4.23,0.48,0.12,'proj'); v('Cassete 50 % (9 L)',9,4.47,0.8,0.5,'proj')
v('Bagagem na garagem sob a cama',120,5.9,0,0.45,'proj'); v('Mantimentos e utensílios (cozinha)',30,3.2,0.74,0.9,'proj')
v('Roupas e objetos (guarda-roupa/armários)',30,5.2,0.5,1.4,'proj'); v('Cadeiras, mesa externa, equipamentos',25,6.0,0,0.5,'proj')
def resumo(lista):
    m=sum(i['m'] for i in lista); s=sum(i['m']*i['s'] for i in lista)/m; x=sum(i['m']*i['x'] for i in lista)/m; h=sum(i['m']*i['h'] for i in lista)/m
    # inertia about CG, axes: X long (s), Y lat (x), Z vert (h)
    Ixx=Iyy=Izz=0
    for i in lista:
        ds,dx,dh=i['s']-s,i['x']-x,i['h']-h; mm=i['m']
        Ixx+=mm*(dx*dx+dh*dh)+mm*(i['dx']**2+i['dh']**2)/12
        Iyy+=mm*(ds*ds+dh*dh)+mm*(i['ds']**2+i['dh']**2)/12
        Izz+=mm*(ds*ds+dx*dx)+mm*(i['ds']**2+i['dx']**2)/12
    Rr=m*(s-1.2)/4.0; Rf=m-Rr
    hsolo=h+0.19
    return dict(m=m,s=s,x=x,h=h,hsolo=hsolo,Rf=Rf,Rr=Rr,pf=Rf/m,Ixx=Ixx,Iyy=Iyy,Izz=Izz,SSF=1.70/(2*hsolo))
cen={'vazio':resumo(itens),'om':resumo(itens+[i for i in var if i['cen']=='om']),'proj':resumo(itens+var)}
subs={}
for i in itens: subs[i['sub']]=subs.get(i['sub'],0)+i['m']
out=dict(geo=geo,camadas=camadas,kgm2=kgm2,esp=esp,A_ext=A_ext,reg=reg,itens=itens,var=var,cen=cen,subs=subs)
json.dump(out,open(AQUI/'massa.json','w'),indent=1,ensure_ascii=False)
print('geo',{k:round(v,3) for k,v in geo.items()}); print('kg/m2',round(kgm2,2),'esp',esp,'Aext',round(A_ext,2))
for k,v in subs.items(): print(f'{k:22s} {v:7.1f}')
for k,c in cen.items(): print(k,{a:round(b,3) for a,b in c.items()})
print('carcaça',round(A_ext*kgm2,1),'quadro',round(165*0.821*1.1,1),'caixas',round(C['caixas']['area_total']*kgm2,1),'long',round(long,1),'trav',round(trav,1))
