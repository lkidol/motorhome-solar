"""Massas, centro de gravidade e inércias do motorhome.

Lê a aba Materiais de plan/Inventario_de_Massas_Motorhome_Solar.xlsx (exportação da planilha
"Inventário de Massas — Motorhome Solar" do Google, que é a fonte oficial) e refaz as contas da
aba Resumo: cenários vazio, em ordem de marcha e carregado. Gera massa.json, usado por estrut.py.

Coordenadas: s da frente (m), x lateral (+ à esquerda), h do fundo da carcaça; h do solo = h + vão livre.
"""
import json, pathlib, openpyxl

AQUI = pathlib.Path(__file__).resolve().parent
XLSX = AQUI.parent / 'plan' / 'Inventario_de_Massas_Motorhome_Solar.xlsx'

wb = openpyxl.load_workbook(XLSX, data_only=True)
proj = {r[0]: r[1] for r in wb['Projeto'].iter_rows(min_row=2, max_row=13, max_col=2, values_only=True) if r[0]}
VAO = float(proj['Vão livre (fundo ao solo)'])
S_F, S_T = float(proj['Eixo dianteiro (s)']), float(proj['Eixo traseiro (s)'])
BITOLA = float(proj['Bitola (centro dos pneus)'])

CEN = {'Vazio': 'vazio', 'Ordem de marcha': 'om', 'Carregado': 'proj'}
itens, var = [], []
for r in wb['Materiais'].iter_rows(min_row=2, max_col=17, values_only=True):
    if not r[0] or r[3] is None or r[4] is None:
        continue
    sub, nome, mat, q, mu, _, cen, s, x, px, h, ds, dx, dh, ns, origem, obs = r
    i = dict(sub=sub, nome=nome, mat=mat or '', m=float(q) * float(mu), s=float(s), x=float(x), px=float(px or 0),
             h=float(h), ds=float(ds or 0), dx=float(dx or 0), dh=float(dh or 0), naoSusp=bool(ns), origem=origem, cen=CEN[cen])
    (itens if cen == 'Vazio' else var).append(i)

def resumo(lista):
    m = sum(i['m'] for i in lista)
    s = sum(i['m'] * i['s'] for i in lista) / m
    x = sum(i['m'] * i['x'] for i in lista) / m
    hs = sum(i['m'] * (i['h'] + VAO) for i in lista) / m
    # inércias no CG (eixos: xx rolagem, yy arfagem, zz guinada), como na aba Resumo
    Ss = sum(i['m'] * i['s'] ** 2 for i in lista)
    Sx = sum(i['m'] * (i['x'] ** 2 + i['px'] ** 2) for i in lista)
    Sh = sum(i['m'] * (i['h'] + VAO) ** 2 for i in lista)
    Ixx0 = sum(i['m'] * (i['dx'] ** 2 + i['dh'] ** 2) / 12 for i in lista)
    Iyy0 = sum(i['m'] * (i['ds'] ** 2 + i['dh'] ** 2) / 12 for i in lista)
    Izz0 = sum(i['m'] * (i['ds'] ** 2 + i['dx'] ** 2) / 12 for i in lista)
    Rf = m * (S_T - s) / (S_T - S_F)
    return dict(m=m, s=s, x=x, h=hs - VAO, hsolo=hs, Rf=Rf, Rr=m - Rf, pf=Rf / m,
                Ixx=Sx + Sh + Ixx0 - m * (x ** 2 + hs ** 2), Iyy=Ss + Sh + Iyy0 - m * (s ** 2 + hs ** 2),
                Izz=Ss + Sx + Izz0 - m * (s ** 2 + x ** 2), SSF=BITOLA / (2 * hs))

om = [i for i in var if i['cen'] == 'om']
cen = {'vazio': resumo(itens), 'om': resumo(itens + om), 'proj': resumo(itens + var)}
subs = {}
for i in itens + var:
    subs[i['sub']] = subs.get(i['sub'], 0) + i['m']
json.dump(dict(fonte=str(XLSX.relative_to(AQUI.parent)), itens=itens, var=var, cen=cen, subs=subs),
          open(AQUI / 'massa.json', 'w'), indent=1, ensure_ascii=False)
for k, v in subs.items():
    print(f'{k:22s} {v:7.1f}')
for k, c in cen.items():
    print(k, {a: round(b, 3) for a, b in c.items()})
