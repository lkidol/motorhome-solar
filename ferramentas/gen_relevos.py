"""Gera relevos.json: peças externas em relevo que seguem a superfície do carcaca.stl.
Coordenadas de projeto: s (da frente), x (+ esquerda), h (do fundo). Mundo: (s-3.5, h+0.19, x)."""
import sys, json, base64, math
sys.path.insert(0, '/home/claude/geo')
import numpy as np
from secoes import M, VAO

img = np.load('/home/claude/geo/lado.npy')
S = np.arange(-0.02, 7.03, 0.01); H = np.arange(-0.02, 2.42, 0.01)
ok = img > 0.9

# parede lateral: as laterais são verticais, então x depende só de s
_wall = np.full(len(S), np.nan)
for j in range(len(S)):
    v = img[:, j][ok[:, j]]
    if len(v): _wall[j] = np.median(v)
_valid = ~np.isnan(_wall)
def wallS(s): return float(np.interp(s, S[_valid], _wall[_valid]))
def topoLado(s):
    j = int(round((s - S[0]) / 0.01)); hs = H[ok[:, j]]; return float(hs.max())
def fundoLado(s):
    j = int(round((s - S[0]) / 0.01)); hs = H[ok[:, j] & (H > 0.04)]; return float(hs.min())

def ray(o, d):
    loc, ri, ti = M.ray.intersects_location([o], [d], multiple_hits=False)
    return (loc[0], ti[0]) if len(loc) else (None, None)
def frente(x, h):
    p, t = ray([-6, h + VAO, x], [1, 0, 0]); return None if p is None else p[0] + 3.5
def tras(x, h):
    p, t = ray([6, h + VAO, x], [-1, 0, 0]); return None if p is None else p[0] + 3.5

Wd = lambda s, x, h: [s - 3.5, h + VAO, x]

pecas = []
def malha(rings, closed_profile=False, caps=True, hard=True):
    """rings: lista de anéis (cada um lista de pontos 3D). Faixas separadas por segmento do perfil (quinas vivas)."""
    R = np.array(rings, dtype=np.float32)  # [n_path, n_prof, 3]
    n, m, _ = R.shape
    pos = []; idx = []
    segs = list(range(m - 1)) + ([m - 1] if closed_profile else [])
    for k in segs:
        k2 = (k + 1) % m
        base = len(pos) // 3
        for i in range(n):
            pos += list(R[i, k]) + list(R[i, k2])
        for i in range(n - 1):
            a = base + 2 * i
            idx += [a, a + 2, a + 1, a + 1, a + 2, a + 3]
    if caps:
        for i in (0, n - 1):
            base = len(pos) // 3
            for k in range(m): pos += list(R[i, k])
            c = R[i].mean(0); ci = len(pos) // 3; pos += list(c)
            for k in range(m):
                a, b = base + k, base + (k + 1) % m
                idx += ([ci, a, b] if i == 0 else [ci, b, a])
    return pos, idx

def add(id_, mat, partes):
    pos = []; idx = []
    for p, ix in partes:
        b = len(pos) // 3; pos += p; idx += [b + v for v in ix]
    pecas.append({'id': id_, 'mat': mat,
                  'pos': base64.b64encode(np.array(pos, np.float32).tobytes()).decode(),
                  'idx': base64.b64encode(np.array(idx, np.uint32).tobytes()).decode(),
                  'n': len(idx) // 3})

def lateral(path, prof, lado, normal=None, parede=None):
    """path: [(s,h)], prof: [(u,o)] u no plano s-h ao longo da normal do caminho, o para fora da parede."""
    P = np.array(path, float); rings = []
    for i, (s, h) in enumerate(P):
        if normal is not None: N = normal(i, s, h)
        else:
            t = P[min(i + 1, len(P) - 1)] - P[max(i - 1, 0)]; t /= np.linalg.norm(t); N = np.array([-t[1], t[0]])
        ring = []
        for u, o in prof:
            ss, hh = s + u * N[0], h + u * N[1]
            ring.append(Wd(ss, lado * ((parede if parede is not None else wallS(ss)) + o), hh))
        rings.append(ring)
    return malha(rings)

# ---------- 1. alargadores dos para-lamas ----------
FLARE = [(-0.004, -0.015), (-0.004, 0.012), (0.004, 0.024), (0.02, 0.032), (0.05, 0.030), (0.072, 0.016), (0.08, -0.012)]
def arco(sc, th0, th1, r0=0.502, n=60):
    th = np.radians(np.linspace(th0, th1, n))
    return [(sc + r0 * math.cos(t), 0.20 + r0 * math.sin(t)) for t in th], th
for id_, sc, th0, th1 in [('alargD', 1.2, 200, -20), ('alargT', 5.2, 200, 9)]:
    partes = []
    for lado in (1, -1):
        path, th = arco(sc, th0, th1)
        partes.append(lateral(path, FLARE, lado, normal=lambda i, s, h, th=th: np.array([math.cos(th[i]), math.sin(th[i])])))
    add(id_, 'clad', partes)

# ---------- 2. soleiras laterais (entre as rodas) ----------
SOL = [(0.0, -0.012), (0.0, 0.026), (0.012, 0.036), (0.125, 0.036), (0.155, 0.024), (0.175, 0.004), (0.18, -0.012)]
partes = []
for lado in (1, -1):
    path = [(s, -0.005) for s in np.linspace(1.665, 4.735, 80)]
    partes.append(lateral(path, SOL, lado, normal=lambda i, s, h: np.array([0.0, 1.0])))
add('soleira', 'clad', partes)

# ---------- 3. acabamento da traseira baixa (segue o fundo que sobe) ----------
pts = [(s, fundoLado(s)) for s in np.arange(5.72, 6.96, 0.02)]
PERF = [(-0.012, -0.012), (-0.012, 0.02), (0.0, 0.03), (0.07, 0.026), (0.095, 0.01), (0.1, -0.012)]
partes = []
for lado in (1, -1):
    partes.append(lateral(pts, PERF, lado, normal=lambda i, s, h: np.array([-0.44, 0.9]) / np.hypot(0.44, 0.9)))
add('saiaT', 'clad', partes)

# ---------- 4. vinco de ombro (na cor do carro), cortado nas portas; o trecho das portas vai junto com elas ----------
VIN = [(-0.014, -0.004), (-0.009, 0.004), (0.0, 0.009), (0.007, 0.005), (0.012, -0.004)]
def vin(a, b, lado, parede=None):
    path = [(s_, 0.86) for s_ in np.linspace(a, b, max(4, int((b - a) / 0.04)))]
    return lateral(path, VIN, lado, normal=lambda i, s, h: np.array([0.0, 1.0]), parede=parede)
add('vinco', 'pint', [vin(0.68, 1.751, 1), vin(2.556, 6.95, 1), vin(0.68, 1.751, -1), vin(2.556, 2.701, -1), vin(3.706, 6.95, -1)])
for porta, (a, b), lado in [('portaE', (1.762, 2.545), 1), ('portaD', (1.762, 2.545), -1), ('portaCasa', (2.712, 3.695), -1)]:
    add('vinco|' + porta, 'pint', [vin(a, b, lado, parede=wallS((a + b) / 2 - 0.004 if False else (1.755 + 2.552) / 2 if porta != 'portaCasa' else (2.705 + 3.702) / 2))])

# ---------- 5. calhas do teto ----------
CAL = [(-0.004, -0.008), (-0.004, 0.014), (0.006, 0.018), (0.012, 0.012), (0.012, -0.008)]
partes = []
for lado in (1, -1):
    path = [(s, topoLado(s) - 0.045) for s in np.arange(1.98, 6.62, 0.02)]
    partes.append(lateral(path, CAL, lado))
add('calha', 'preto', partes)
# calha sobre a janela da sala (lado direito)
add('calhaJ', 'preto', [lateral([(s, 1.935) for s in np.linspace(3.76, 4.85, 30)], CAL, -1, normal=lambda i, s, h: np.array([0.0, 1.0]))])

# ---------- 6. caixa do toldo (lado direito, sobre a porta de entrada) ----------
TOL = [(0.0, -0.01)] + [(0.0 + 0.045 - 0.045 * math.cos(a), 0.055 + 0.045 * math.sin(a)) for a in np.linspace(-math.pi / 2, math.pi / 2, 9)][::-1]
TOL = [(0.0, -0.01), (0.0, 0.01)] + [(0.05 - 0.05 * math.cos(a), 0.05 + 0.05 * math.sin(a)) for a in np.linspace(0, math.pi, 11)] + [(0.1, 0.0), (0.1, -0.01)]
# perfil em (u para cima, o para fora): base em h=2.055
path = [(s, 2.055) for s in np.linspace(2.78, 5.92, 60)]
add('toldo', 'toldo', [lateral(path, [(u, o) for u, o in TOL], -1, normal=lambda i, s, h: np.array([0.0, 1.0]))])
# tampas das pontas
partes = []
for s0 in (2.765, 5.92):
    rings = []
    for ds in (0.0, 0.015):
        rings.append([Wd(s0 + ds, -(wallS(s0) + o + 0.004), 2.055 + u - 0.004 + (0.008 if u > 0.05 else 0)) for u, o in TOL])
    partes.append(malha(rings))
add('toldo', 'preto', partes)

# ---------- 7. para-choque dianteiro: lábio, entradas de ar laterais, aletas da tomada de ar ----------
# lábio (splitter) logo abaixo do nariz
xs = np.linspace(-0.98, 0.98, 49)
fr0 = [frente(x, 0.02) for x in xs]
rings = []
for x, f in zip(xs, fr0):
    rings.append([Wd(f + 0.10, x, -0.012), Wd(f - 0.045, x, -0.012), Wd(f - 0.05, x, 0.0), Wd(f - 0.04, x, 0.012), Wd(f + 0.10, x, 0.012)])
add('labio', 'preto', [malha(rings)])
# entradas de ar dos cantos (cortina de ar), seguindo a superfície inclinada do nariz
partes = []; grades = []
for lado in (1, -1):
    xa, xb = 0.64, 0.88; ha, hb = 0.13, 0.33
    # moldura: retângulo arredondado traçado na superfície, perfil para fora (-s)
    def sp(x, h, o):
        f = frente(lado * x, h); return Wd(f - o, lado * x, h)
    per = []
    for x in np.linspace(xa, xb, 12): per.append((x, ha))
    for h in np.linspace(ha, hb, 10)[1:]: per.append((xb, h))
    for x in np.linspace(xb, xa, 12)[1:]: per.append((x, hb))
    for h in np.linspace(hb, ha, 10)[1:-1]: per.append((xa, h))
    rings = []
    cx, ch = (xa + xb) / 2, (ha + hb) / 2
    for x, h in per:
        dx, dh = (x - cx) / (xb - xa), (h - ch) / (hb - ha)
        ux, uh = (math.copysign(1, dx), 0.0) if abs(dx) >= abs(dh) else (0.0, math.copysign(1, dh))
        rings.append([sp(x - 0.012 * ux, h - 0.012 * uh, -0.006), sp(x - 0.012 * ux, h - 0.012 * uh, 0.008), sp(x + 0.01 * ux, h + 0.01 * uh, 0.012), sp(x + 0.022 * ux, h + 0.022 * uh, 0.002), sp(x + 0.022 * ux, h + 0.022 * uh, -0.006)])
    rings.append(rings[0])
    partes.append(malha(rings, caps=False))
    # fundo escuro da entrada (levemente recuado) com 3 aletas
    rings = []
    for h in np.linspace(ha + 0.012, hb - 0.012, 8):
        rings.append([sp(x, h, -0.004) for x in np.linspace(xa + 0.012, xb - 0.012, 8)])
    grades.append(malha(rings, caps=False))
    for hh in np.linspace(ha + 0.05, hb - 0.05, 3):
        rings = []
        for x in np.linspace(xa + 0.012, xb - 0.012, 10):
            rings.append([sp(x, hh - 0.006, -0.004), sp(x, hh - 0.003, 0.008), sp(x, hh + 0.003, 0.008), sp(x, hh + 0.006, -0.004)])
        partes.append(malha(rings))
add('entradas', 'preto', partes)
add('entradas', 'grade', grades)
# aletas horizontais sobre a tomada de ar do radiador
partes = []
for hh in (0.475, 0.535, 0.595, 0.655):
    rings = []
    for x in np.linspace(-0.40, 0.40, 33):
        f = frente(x, hh)
        rings.append([Wd(f + 0.004, x, hh - 0.012), Wd(f - 0.012, x, hh - 0.008), Wd(f - 0.014, x, hh + 0.004), Wd(f + 0.004, x, hh + 0.01)])
    partes.append(malha(rings))
add('aletas', 'preto', partes)

# ---------- 8. para-choque traseiro, refletores, difusor e aerofólio ----------
# para-choque: percorre a lateral esquerda (6,72→7,0), a traseira e volta pela direita
BUMP = [(-0.02, -0.012), (-0.02, 0.05), (-0.006, 0.066), (0.10, 0.07), (0.13, 0.058), (0.14, 0.03), (0.14, -0.012)]  # (dh, saliência)
hb0 = 0.875
def bump_ring_side(s, lado):
    return [Wd(s, lado * (wallS(s) + o), hb0 + dh) for dh, o in BUMP]
def bump_ring_rear(x, n_hint):
    return [Wd(tras(x, hb0 + 0.07) + o, x, hb0 + dh) for dh, o in BUMP]
rings = []
for s in np.linspace(6.80, 6.985, 8): rings.append(bump_ring_side(s, 1))
for x in np.linspace(0.90, -0.90, 41): rings.append(bump_ring_rear(x, 0))
for s in np.linspace(6.985, 6.80, 8): rings.append(bump_ring_side(s, -1))
add('parachoqueT', 'clad', [malha(rings)])
# refletores vermelhos (obrigatórios) nas pontas do para-choque
partes = []
for lado in (1, -1):
    for x0 in (0.70,):
        x = lado * x0; f = tras(x, hb0 + 0.07) + 0.0705
        rings = [[Wd(f, x - 0.06, hb0 + 0.03), Wd(f, x + 0.06, hb0 + 0.03), Wd(f + 0.004, x + 0.06, hb0 + 0.05), Wd(f + 0.004, x - 0.06, hb0 + 0.05)]]
        rings.append([Wd(f + 0.004, x - 0.06, hb0 + 0.075), Wd(f + 0.004, x + 0.06, hb0 + 0.075), Wd(f, x + 0.06, hb0 + 0.09), Wd(f, x - 0.06, hb0 + 0.09)])
        partes.append(malha(rings))
add('refletorT', 'refletor', partes)
# aletas do difusor sob a traseira que sobe
partes = []
for x in (-0.62, -0.22, 0.22, 0.62):
    rings = []
    for s in np.arange(5.95, 6.90, 0.025):
        hb = fundoLado(s) + 0.01
        rings.append([Wd(s, x - 0.006, hb), Wd(s, x - 0.006, hb - 0.07), Wd(s, x + 0.006, hb - 0.07), Wd(s, x + 0.006, hb)])
    partes.append(malha(rings))
add('difusor', 'clad', partes)
# aerofólio no alto da traseira (abriga a 3ª luz de freio)
rings = []
for x in np.linspace(-0.82, 0.82, 33):
    rings.append([Wd(6.86, x, 1.905), Wd(7.075, x, 1.915), Wd(7.08, x, 1.928), Wd(6.86, x, 1.935)])
add('aerofolio', 'preto', [malha(rings)])

# ---------- 9. lanternas laterais âmbar (veículo > 6 m) ----------
partes = []
for lado in (1, -1):
    for s0, h0 in ((4.25, 0.28), (6.42, 0.64)):
        w = wallS(s0)
        rings = [[Wd(s0 - 0.035, lado * (w - 0.002), h0 - 0.012), Wd(s0 - 0.035, lado * (w + 0.007), h0 - 0.010), Wd(s0 - 0.035, lado * (w + 0.007), h0 + 0.010), Wd(s0 - 0.035, lado * (w - 0.002), h0 + 0.012)],
                 [Wd(s0 + 0.035, lado * (w - 0.002), h0 - 0.012), Wd(s0 + 0.035, lado * (w + 0.007), h0 - 0.010), Wd(s0 + 0.035, lado * (w + 0.007), h0 + 0.010), Wd(s0 + 0.035, lado * (w - 0.002), h0 + 0.012)]]
        partes.append(malha(rings))
add('lateralAmb', 'seta', partes)

json.dump(pecas, open('/home/claude/motorhome/relevos.json', 'w'))
print('ok', [(p['id'], p['mat'], p['n']) for p in pecas])
print('wall 1.2', wallS(1.2), 'wall 5.2', wallS(5.2), 'tras', tras(0, 0.95), tras(0.9, 0.95), 'topo 4', topoLado(4.0))
