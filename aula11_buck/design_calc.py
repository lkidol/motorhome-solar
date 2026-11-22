"""Analytical sizing + loss budget for the 24 V -> 12 V Buck (Aula 11)."""
import math

Vin, Vo, fs = 24.0, 12.0, 20e3
dI_max, dV_max = 0.40, 0.12
R_light, R_nom = 12.0, 6.0

D = Vo / Vin
L_min = (Vin - Vo) * D / (fs * dI_max)
L_crit = (1 - D) * R_light / (2 * fs)
print(f"D={D:.3f}  L_min={L_min*1e6:.0f} uH  L_crit(12ohm)={L_crit*1e6:.0f} uH")

rC = 0.130   # ohm, ESR candidate (distributor listing, to confirm)
C_noESR = dI_max / (8 * fs * dV_max)
C_ESR = dI_max / (8 * fs * (dV_max - rC * dI_max))
C_ESR100 = dI_max / (8 * fs * (dV_max - 0.100 * dI_max))
print(f"C_min(no ESR)={C_noESR*1e6:.1f} uF  C_min(rC=0.1)={C_ESR100*1e6:.1f} uF  C_min(rC=0.13)={C_ESR*1e6:.1f} uF")
print("ESR max for C=100uF, dI=0.4: %.3f ohm" % ((dV_max - dI_max/(8*fs*100e-6))/dI_max))

L = 1e-3; C = 100e-6
dI = (Vin - Vo) * D / (L * fs)
print(f"L=1mH: dI={dI:.3f} A; ILmin(12ohm)={1-dI/2:.3f}; ILpk(2A)={2+dI/2:.3f}; ILrms(2A)={math.sqrt(4+dI**2/12):.4f}")
dv_cap = dI / (8 * fs * C)
print(f"C=100uF: dv_cap={dv_cap*1e3:.2f} mV; bound with rC=.13: {(dv_cap+rC*dI)*1e3:.1f} mV; ICrms={dI/math.sqrt(12):.3f} A")
print("L=470u,C=22u: dI=%.3f dv(no ESR)=%.3f" % ((Vin-Vo)*D/(470e-6*fs), ((Vin-Vo)*D/(470e-6*fs))/(8*fs*22e-6)))

# ---- loss budget at Io=2 A, commercial parameters ----
Io = 2.0
RDS = 0.020; RDS_hot = 0.035
VF = 0.525; rL = 0.195
Qg, Vgs = 63e-9, 12.0
Qgd = 23e-9
tr, tf = 60e-9, 45e-9
Po = Vo * Io
Dn = (Vo + VF + Io * rL) / (Vin + VF - Io * RDS)
Irms2 = Io**2 + dI**2 / 12
for name, rds in (("RDS=20mOhm", RDS), ("RDS=35mOhm (hot)", RDS_hot)):
    P_cond = rds * Dn * Irms2
    P_d = VF * (1 - Dn) * Io
    P_L = rL * Irms2
    P_C = rC * dI**2 / 12
    P_drv = Qg * Vgs * fs
    for tag, tsw in (("datasheet tr+tf", tr + tf), ("IR2104 130/270mA", Qgd/0.130 + Qgd/0.270)):
        P_sw = 0.5 * Vin * Io * tsw * fs
        Ploss = P_cond + P_d + P_L + P_C + P_drv + P_sw
        print(f"{name} | {tag}: D={Dn:.4f} Pcond={P_cond:.3f} Pdiode={P_d:.3f} PL={P_L:.3f} PC={P_C*1e3:.2f}mW Psw={P_sw:.3f} Pdrv={P_drv*1e3:.1f}mW  Ploss={Ploss:.3f}  eta={Po/(Po+Ploss)*100:.2f}%")
# sensitivity to fs
for f in (10e3, 20e3, 50e3, 100e3):
    dIf = (Vin - Vo) * D / (L * f)
    Psw = 0.5 * Vin * Io * (Qgd/0.130 + Qgd/0.270) * f
    print(f"fs={f/1e3:.0f}kHz dI(L=1mH)={dIf:.3f} A  dv_cap(C=100u)={dIf/(8*f*C)*1e3:.1f} mV  Psw={Psw:.3f} W  Pdrv={Qg*Vgs*f*1e3:.1f} mW")
# bootstrap cap
print("Cboot >= %.0f nF (dV=0.5V, x2 margin)" % (2*Qg/0.5*1e9))
# D compromise
D_nom = Dn
for Dx in (D_nom, D_nom - 0.0025):
    v12 = (Dx*Vin-(1-Dx)*VF)/(1+(Dx*RDS+rL)/12); v6 = (Dx*Vin-(1-Dx)*VF)/(1+(Dx*RDS+rL)/6)
    print(f"D={Dx:.4f}: vo(12)={v12:.3f} vo(6)={v6:.3f}")
