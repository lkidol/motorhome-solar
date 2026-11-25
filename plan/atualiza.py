"""LEGADO: gera a planilha antiga (aba Materiais simples) a partir de original.xlsx.

A planilha oficial agora é a "Inventário de Massas — Motorhome Solar" do Google; o arquivo
Inventario_de_Massas_Motorhome_Solar.xlsx desta pasta é uma exportação dela. Este script grava em
outro nome para não sobrescrever a exportação.
"""
import openpyxl, copy, pathlib
AQUI=pathlib.Path(__file__).resolve().parent
from openpyxl.worksheet.datavalidation import DataValidation
wb=openpyxl.load_workbook(AQUI/'original.xlsx')
ws=wb['Materiais']
# guarda as linhas da Elétrica exatamente como estão (dados do grupo)
eletr=[[ws.cell(r,c).value for c in range(1,8)] for r in range(2,31) if ws.cell(r,1).value=='Elétrica']
chuv=[[ws.cell(r,c).value for c in range(1,8)] for r in range(2,31) if ws.cell(r,2).value=='Chuveiro elétrico / aquecimento de água'][0]
redut=[[ws.cell(r,c).value for c in range(1,8)] for r in range(2,31) if ws.cell(r,2).value=='Redutor / transmissão'][0]
estilo=[copy.copy(ws.cell(2,c)._style) for c in range(1,8)]
LEV='Levantamento mecânico do projeto'
TER='Inventário térmico (itens 11, 30 a 35)'
M,T,H,I,O='Mecânica','Térmica','Hidráulica','Interiores','Outros'
linhas=[
 [M,'Casca da carroceria (sem portas)','Painel sanduíche 30 mm: Al 5754-H22 3 mm + PU + núcleo PIR 23 mm (35 kg/m³) + PU + compensado de choupo 3 mm = 11,54 kg/m²',1,588.46,LEV+'. Área externa medida no STL: 50,97 m² (laterais 19,23; fundo 13,89; teto 12,94; frente 2,66; traseira 2,25), sem os vãos de portas e janela'],
 [M,'Quadro de perfis (cavernas e longitudinais)','Al 6063-T6, tubo 40 × 40 × 2 mm (0,82 kg/m), ~165 m',1,149.01,LEV],
 [M,'Caixas de roda','Mesmo sanduíche da carroceria: Al 5754 3 mm + PIR 23 mm + choupo 3 mm (11,54 kg/m²)',4,25.44,LEV+'. 8,82 m² no total. Envoltória definida no inventário térmico (antes: chapa de Al 3 mm)'],
 [M,'Adesivos, selantes e rebites','PU / MS polímero',1,18,LEV],
 [M,'Portas da cabine (motorista e passageiro)','Sanduíche 30 mm + vidro temperado 4 mm + dobradiças e fechadura',2,23.60,LEV+'. 1,33 m² cada, vidro 0,48 m²'],
 [M,'Porta de entrada','Sanduíche 30 mm + vidro temperado 4 mm + dobradiças e fechadura',1,31.43,LEV+'. 1,75 m², vidro 0,48 m²'],
 [M,'Para-brisa','Vidro laminado 5 mm (2 × 2,1 mm + PVB 0,76 mm), 3,25 m²',1,40.63,LEV],
 [M,'Janela da sala (2 folhas)','Acrílico duplo PMMA 2 × 3 mm + caixilho, 0,91 m²',1,10.80,LEV],
 [M,'Longarinas do chassi','Al 6061-T6, tubo retangular 250 × 80 × 6 mm, 6,6 m cada',2,68.00,LEV+'. O perfil 150 × 60 × 5 mm não passou na verificação (FS 0,47), por isso o 250 × 80 × 6'],
 [M,'Travessas do chassi','Al 6061-T6, tubo 100 × 50 × 4 mm, 1,9 m cada',8,5.83,LEV],
 [M,'Subchassi dianteiro','Aço S355 soldado (torres da suspensão e direção)',1,60,LEV],
 [M,'Subchassi traseiro','Aço S355 soldado (motor e suspensão)',1,55,LEV],
 [M,'Berço e chapa de proteção da bateria','Al 5083 5 mm + quadro em 6061',1,47,LEV],
 [M,'Barras de impacto, engate e suportes','Aço / alumínio',1,25,LEV],
 [M,'Piso elevado estrutural','Painel colmeia de alumínio 20 mm (5 kg/m²) + apoios, topo a 0,30 m do fundo',1,42.5,LEV],
 [M,'Rodas e pneus','Roda de aço 17,5 × 6,75 + pneu 245/70 R17.5 (Ø 0,788 m, índice de carga 136/134)',4,48,LEV],
 [M,'Estepe','Mesma roda e pneu, deitado sob a cama (ou trocar por kit de reparo)',1,48,LEV],
 [M,'Freios (cubo, disco ventilado e pinça)','Disco de referência Iveco Daily 70C15: Ø 306 × 28 mm, ventilado, ferro fundido EN-GJL-250 + pinça de aço',4,16,LEV+'. Disco do item 33: 223 °C no fim da frenagem de 30 para 10 m/s, sem regeneração'],
 [M,'Suspensão dianteira','Braços, molas e amortecedores',1,90,LEV],
 [M,'Suspensão traseira','Independente: braços, molas e amortecedores',1,100,LEV],
 [M,'Direção','Caixa com assistência elétrica + coluna e barras',1,25,LEV],
 [M,'Redutor 8:1 com diferencial','Modelo comercial a definir; carcaça de alumínio, 450 × 350 × 300 mm (hipótese), 2,5 L de óleo',1,60,'Item 12: dimensões e massa como hipótese (25 kg de alumínio e 35 kg de aço). Antes: relação 15:1 e 40 kg. O motor fica na Elétrica'],
 [M,'Semieixos','Aço forjado',2,9,LEV],
 [M,'Para-choques, alargadores, soleiras, saias, difusor e aerofólio','PP-EPDM (TPO) 3 mm + suportes',1,60,LEV],
 [M,'Carenagem lateral do teto','Al 1,5 mm',1,10,LEV],
 [M,'Estrutura do painel solar fixo e das gavetas (sem os módulos)','Suporte Al do painel fixo 4,40 × 2,00 m + 2 gavetas de 3,40 × 1,30 m com trilhos e atuadores',1,74.2,LEV+'. Os módulos estão na linha Painéis solares (Elétrica)'],
]
ELETR={  # atualizações do inventário térmico (itens 10, 30, 34 e 35); o resto da aba Elétrica fica como o grupo mandou
 'Motor elétrico de tração':(None,'Cascadia SS-320-180, ≈ 460 V CA de linha; lubrificado e resfriado por ATF com trocador óleo-água',None,None,'. Modelo definido nos itens 10, 12 e 35'),
 'Células do banco de alta tensão':(None,'Pouch NCM equivalente à LG Energy Solution E65D, 3,67 V nominal, 354 × 101 × 11,5 mm (203,6 kWh no total)',764,0.906,' → substituída pelo inventário térmico (itens 10 e 34): 764 células NCM de 0,906 kg. Conferir a contagem de células na K5 da Planilha Geral'),
 'Inversor de tração':(None,'Cascadia CM350SiC, 649 V CC, 500 A contínuos (corrente limitada em ≈ 400 A por causa dos cabos de fase)',None,None,'. Modelo definido nos itens 30 e 35'),
 'Controlador de carga solar (MPPT)':('Conversor solar BrightLoop DCHV','Refrigerado a líquido no circuito do motor, rendimento de 97 %',None,None,'. Modelo definido no item 10; massa ainda estimada'),
 'Cabeamento, proteções e carregador':(None,None,None,None,'. Cabos de fase: Coroplast 9-2611 FHLR2GCB2G 70 mm² blindado, T180 (item 30)'),
}
for r in eletr:
    if r[1]=='Painéis solares': r=r[:6]+[r[6]+'. Área no teto: 8,8 m² fixos + 2 × 4,42 m² nas gavetas = 17,7 m² estacionado']
    if r[1] in ELETR:
        nome,mat,q,m,obs=ELETR[r[1]]; r=list(r)
        if nome: r[1]=nome
        if mat: r[2]=mat
        if q is not None: r[3]=q
        if m is not None: r[4]=m
        r[6]=(r[6] or '')+obs
    linhas.append(r)
linhas+=[
 [T,'Ar-condicionado / bomba de calor Dometic FreshWell 3000 (FWX4350)','628 × 400 × 286 mm, 990 W em 230 V CA; 2,7 kW de frio e 3,0 kW de calor cada (COP 2,73). Sob o painel, no lugar da caixa 71',2,21,TER+'. Catálogo Jacksons/Frankana. Antes: 1 unidade de 3.000 W e 30 kg'],
 [T,'Dutos de insuflamento, grelhas do condensador e dreno de condensado','Dutos do FreshWell até o painel; 2 grelhas no fundo',1,None,TER+'. Massa não levantada'],
 [T,'Exaustor de teto MaxxAir MaxxFan Deluxe 00-05100K','589 × 421 × 128 mm, 12 V CC, 30 W, com comando remoto; furo de 356 × 356 mm no teto traseiro',1,5.4,TER+'. 15 L/s de ar externo para 2 ocupantes'],
 [T,'Grelha de entrada de ar externo','Passiva com filtro, 300 × 120 mm, lateral direita',1,None,TER+'. Hipótese'],
 [T,'Películas de controle solar','3M Crystalline aplicada por dentro: CR 70 no para-brisa e nas portas da cabine (≈ 4,2 m², VLT 78 %) e CR 30 na porta de entrada e na janela da sala (≈ 1,4 m²)',1,None,TER+'. CONTRAN 960/2022 exige VLT ≥ 70 % no para-brisa e nas portas da cabine. A carga do ar-condicionado cai de 4,5 para 3,5 kW'],
 chuv,
 [T,'Isolamento térmico','Núcleo PIR 23 mm do painel sanduíche',1,0,'Já está na casca da carroceria (Mecânica): 0,8 kg/m² × 51 m² ≈ 41 kg. Fica zerado para não contar duas vezes'],
 [T,'Radiador do motor, inversor e bateria','Fabricação sob medida: núcleo 800 × 400 × 66 mm, Al brasado, fluxo cruzado em 4 passes; módulo de 880 × 175 × 420 mm com ventiladores',1,8,TER+' (item 35): UA = 622 W/K, rejeita 15,6 kW. Sem chiller. Massa estimada'],
 [T,'Ventiladores do radiador SPAL VA18-AP71/LL-59A (16")','Aspirantes, 12 V CC, 250 W cada',2,2.57,TER+'. 5.470 m³/h com os dois'],
 [T,'Bomba principal de arrefecimento Pierburg CWA 150','12 V CC, 180 W',1,1,TER],
 [T,'Bomba do circuito da bateria Rheinmetall CWP 50','12 V CC, 54 W',1,0.6,TER+'. Massa estimada'],
 [T,'Válvula de 3 vias Rheinmetall (Pierburg)','12 V CC, ≈ 5 W; comuta a bateria entre série e desvio',1,0.4,TER+'. Massa e potência estimadas'],
 [T,'Placas frias da bateria','Alumínio, 1250 × 1560 × 6 mm, 120 canais de 10 × 3 mm, 5 L/min por placa',2,19.4,TER+' (item 34)'],
 [T,'Material de interface (gap filler)','DOWSIL TC-5515 LT, 1,5 mm sob as 764 células',1,9,TER],
 [T,'Fluido de arrefecimento','Etilenoglicol (ASTM D3306) a 50 % em água, 19,8 L',1,21,TER],
 [T,'Mangueiras','EPDM automotiva, 4 m de Ø 25 mm e 12 m de Ø 16 mm',1,4.8,TER+'. Hipótese; massa estimada. Traçado ainda não está no STL'],
 [T,'Reservatório de expansão','Automotivo, 1 L, com tampa pressurizada',1,0.5,TER+'. Hipótese'],
 [T,'Sensores de temperatura do arrefecimento','NTC automotivo, rosca M12',4,None,TER],
 [T,'Óleo do motor (ATF)','Mobil Dexron-VI ATF, ≈ 4,6 L',1,3.8,TER+' (item 12). Volume estimado'],
 [T,'Óleo do redutor 8:1 e diferencial','Mobilube 1 SHC 75W-90, ≈ 2,5 L',1,2.2,TER+' (item 12). Volume estimado'],
 [T,'Bomba elétrica auxiliar de óleo','Opcional Cascadia para o SS-320, 12 V CC',1,1,TER+'. Massa estimada'],
 [T,'Sensores de óleo','ACDelco 12677836 (pressão) e 213-4514 (temperatura), 5 V',3,None,TER+'. Acima de 110 °C no óleo do redutor o controle limita a potência a ≈ 60 kW'],
 [H,'Tanque de água limpa (vazio)','PEAD rotomoldado, 100 L, 0,50 × 0,90 × 0,24 m no piso duplo',1,10,LEV+'. A água entra em Outros'],
 [H,'Tanque de águas servidas (vazio)','PEAD, 80 L, 0,50 × 0,75 × 0,24 m no piso duplo',1,8,LEV+'. A água entra em Outros'],
 [H,"Bomba d'água e tubulação",'Bomba, tubos PEX/PP, registros e ralos',1,10,LEV],
 [I,'Piso vinílico e tapete','PVC vinílico 2 mm (3,4 kg/m²)',1,25.8,LEV],
 [I,'Forro do teto','Ripas de madeira 6 mm (3,0 kg/m²)',1,32.9,LEV],
 [I,'Revestimento das paredes','Feltro automotivo 4 mm (0,6 kg/m²)',1,13.2,LEV],
 [I,'Painel de instrumentos, telas e console','PP/ABS + aço + eletrônica',1,45,LEV],
 [I,'Bancos da cabine','Banco automotivo com base giratória e cinto (motorista e passageiro)',2,32,LEV],
 [I,'Volante, pedais e colunas','Aço / alumínio / PU',1,10,LEV],
 [I,'Cooktop de indução Dometic CVI1525','2 zonas (1.000 + 1.300 W), 230 V CA, 525 × 350 × 55 mm',1,6.05,'Ficha técnica Dometic (inventário térmico). Regra de uso: 1 boca no pico'],
 [I,'Móveis da cozinha','Gabinete de choupo 15 mm, tampo de carvalho 35 mm e cuba inox',1,40,LEV],
 [I,'Geladeira Dometic RC 10.4M90','90 L, compressor 12 V CC, 56 W, 420 × 901 × 485 mm',1,21,'Ficha técnica Dometic (inventário térmico)'],
 [I,'Armário aéreo da cozinha','Choupo 12 mm',1,16,LEV],
 [I,'Banheiro: paredes, piso e porta','GRP 4 mm + choupo',1,42,LEV],
 [I,'Banheiro: vaso cassete, pia, armário com espelho, chuveiro e cortina','Vaso Thetford C223-CS (7,2 kg) + ABS / cerâmica / inox',1,30,LEV],
 [I,'Bancos fixos da sala','Banqueta estofada com encosto: estrutura de choupo 15 mm, espuma D33, tecido e cinto',2,22,LEV],
 [I,'Tablado da sala (15,5 cm)','Choupo 18 mm + vinílico + perfil de alumínio na borda',1,8,'Estimativa: 0,55 m² de tampo + laterais. Deixa os dois bancos na mesma altura'],
 [I,'Mesa da sala','Tampo de carvalho 30 mm + coluna inox',1,14,LEV],
 [I,'Guarda-roupa','Choupo 12 mm, sobre a caixa de roda esquerda',1,22,LEV],
 [I,'Degraus e tampa do motor','Choupo 18 mm + carvalho',1,14,LEV],
 [I,'Estrado da cama','Choupo 18 mm',1,26,LEV],
 [I,'Colchão e roupa de cama','Espuma D28 140 mm, 1,4 × 1,9 m + têxteis',1,22,LEV],
 [I,'Armários sobre o pé da cama','Choupo 12 mm, 3 portas',1,14,LEV],
 [I,'Fechamentos, soleiras e forros das caixas de roda','Choupo / ABS + soleiras de alumínio',1,22,LEV],
 [I,'Fitas de LED, luminárias e fiação interna','Alumínio + cobre',1,8,LEV],
 [I,'Cortinas e persianas','Têxtil / plissado',1,8,LEV],
 [O,'Toldo em cassete','3,1 m, alumínio anodizado + lona acrílica',1,26,LEV],
 [O,'Degrau elétrico da porta de entrada','Alumínio + motor 12 V',1,15,LEV],
 [O,'Faróis, lanternas, retrovisores câmera e limpadores','PC/PMMA + eletrônica',1,16,LEV],
 [O,'Ocupantes','Motorista e passageiro',2,75,'Cenário carregado do levantamento. Os 2 bancos fixos da sala também têm cinto: com 4 a bordo, Qtd = 4'],
 [O,'Água limpa','Tanque cheio, 100 L (1 kg por litro)',1,100,LEV],
 [O,'Águas servidas','Tanque pela metade, 40 L',1,40,LEV],
 [O,'Cassete do vaso','Pela metade, 9 L',1,9,LEV],
 [O,'Bagagem','Na garagem sob a cama',1,120,LEV],
 [O,'Mantimentos e utensílios','Cozinha',1,30,LEV],
 [O,'Roupas e objetos','Guarda-roupa e armários',1,30,LEV],
 [O,'Cadeiras, mesa externa e equipamentos','',1,25,LEV],
]
# limpa as linhas antigas e escreve as novas
for r in range(2,ws.max_row+1):
    for c in range(1,8): ws.cell(r,c).value=None
for i,l in enumerate(linhas):
    r=i+2
    for c in range(1,8): ws.cell(r,c)._style=copy.copy(estilo[c-1])
    for c,v in enumerate(l[:5],start=1): ws.cell(r,c).value=v
    if l[4] is None: ws.cell(r,5).value=None
    ws.cell(r,6).value=f'=IF(E{r}="","",D{r}*E{r})'
    ws.cell(r,7).value=l[6] if len(l)>6 else l[5]
last=len(linhas)+1
ws.data_validations.dataValidation=[]
dv=DataValidation(type='list',formula1="'Dropdown options'!$A$1:$A$6",allow_blank=True); dv.add(f'A2:A{last}'); ws.add_data_validation(dv)
print('linhas',len(linhas),'última',last)
# --------- Resumo: dados de referência ---------
rs=wb['Resumo']
h=copy.copy(rs['A3']._style); n=copy.copy(rs['A4']._style); t=copy.copy(rs['A1']._style)
rs['A14']='Dados do projeto (referência)'; rs['A14']._style=copy.copy(t)
for c,v in zip('ABC',['Parâmetro','Valor','Observação']): rs[f'{c}15']=v; rs[f'{c}15']._style=copy.copy(h)
ref=[('Dimensões da carcaça (comp. × larg. × alt.)','7,00 × 2,29 × 2,20 m','Altura total com o painel solar ≈ 2,47 m; largura nos para-lamas ≈ 2,34 m'),
 ('Entre-eixos','4,00 m','Eixos a 1,20 m e 5,20 m da frente'),
 ('Vão livre','0,19 m',''),
 ('Pneus','245/70 R17.5','Ø 0,788 m, índice de carga 136/134'),
 ('Área externa da casca','50,97 m²','Mais 8,82 m² das caixas de roda e 3,25 m² de para-brisa'),
 ('Painel sanduíche da carroceria','30 mm · 11,54 kg/m²','Al 3 mm + PIR 23 mm + compensado 3 mm'),
 ('Longarinas do chassi','250 × 80 × 6 mm','Al 6061-T6'),
 ('Solar fixo (rodando)','8,8 m²','4,40 × 2,00 m, 8 cm acima do teto'),
 ('Gavetas solares','2 × 4,42 m²','3,40 × 1,30 m cada; total estacionado 17,7 m²'),
 ('Espaço da bateria no piso duplo','1,40 × 2,00 × 0,26 m','0,73 m³'),
 ('Bateria de tração','203,6 kWh NCM · 764 células','Equivalente LG E65D; bloco de 1,30 × 1,60 × 0,26 m com 2 placas frias de 1250 × 1560 mm, resfriado pelo radiador do motor (sem chiller)'),
 ('Radiador','Núcleo 800 × 400 × 66 mm','Módulo de 880 × 175 × 420 mm com 2 ventiladores de 16″; tomada de ar de 840 × 280 mm atende até 33 °C de ambiente'),
 ('Climatização','2 × Dometic FreshWell 3000','Sob o painel + MaxxFan Deluxe no teto traseiro; carga de frio de 3,5 kW com as películas 3M'),
 ('Pé-direito na sala','1,87 m','Piso elevado a 0,30 m do fundo'),
 ('PBT proposto','5.000 kg','')]
for i,(a,b,c) in enumerate(ref):
    r=16+i
    for col,v in zip('ABC',(a,b,c)): rs[f'{col}{r}']=v; rs[f'{col}{r}']._style=copy.copy(n)
wb.save(AQUI/'Inventario_de_Massas_legado.xlsx')
