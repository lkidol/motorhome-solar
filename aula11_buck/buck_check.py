"""Independent numerical check of the Buck design (Aula 11, SEM0320).

Same switched model as the MATLAB script (buck_projeto.m); used here only to
cross-check numbers because MATLAB is not available in this environment.
Piecewise integration: q=1 for D*Ts, q=0 for the rest of each period;
iL >= 0 enforced (diode blocks reverse current -> DCM handled by an event).
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from scipy.integrate import solve_ivp

# ---------------- parameters (single place) ----------------
VIN, VO_REF, FS = 24.0, 12.0, 20e3      # V, V, Hz
TS = 1.0 / FS                            # s
T_END, T_STEP = 100e-3, 50e-3            # s
R1, R2 = 12.0, 6.0                       # ohm (before / after step)


@dataclass
class P:
    L: float
    C: float
    rS: float = 0.0
    rL: float = 0.0
    rC: float = 0.0
    VF: float = 0.0


def simulate(p: P, D: float, rtol=1e-8, atol=1e-10):
    """Returns dict of arrays t, iL, vC, vo, q, R (dense, per segment samples)."""
    t_all, iL_all, vC_all, q_all = [], [], [], []
    t, iL, vC = 0.0, 0.0, 0.0
    n_per = int(round(T_END / TS))
    for k in range(n_per):
        t0 = k * TS
        R = R1 if t0 < T_STEP else R2
        for q, dur in ((1, D * TS), (0, (1 - D) * TS)):
            def f(_, x):
                i, v = x
                vo = (v + p.rC * i) / (1 + p.rC / R)
                if q == 1:
                    di = (VIN - p.rS * i - p.rL * i - vo) / p.L
                else:
                    di = (-p.VF - p.rL * i - vo) / p.L if i > 0 else 0.0
                dv = (i - vo / R) / p.C
                return [di, dv]

            def hit0(_, x):
                return x[0]
            hit0.terminal = True
            hit0.direction = -1
            t1 = t + dur
            te = np.linspace(t, t1, 41)
            sol = solve_ivp(f, (t, t1), [iL, vC], t_eval=te, rtol=rtol, atol=atol,
                            events=hit0 if q == 0 else None, max_step=TS / 20)
            tt, ii, vv = sol.t, sol.y[0], sol.y[1]
            if q == 0 and sol.status == 1:       # DCM: iL reached 0
                t_z = sol.t_events[0][0]
                # hold iL = 0, capacitor discharges through load (+rC irrelevant: iL=0)
                def f0(_, x):
                    return [0.0, (-(x[1] / (1 + p.rC / R)) / R) / p.C * 1.0]
                s2 = solve_ivp(f0, (t_z, t1), [0.0, sol.y[1][-1]],
                               t_eval=np.linspace(t_z, t1, 20), rtol=rtol, atol=atol)
                tt = np.r_[tt, s2.t[1:]]
                ii = np.r_[ii, s2.y[0][1:]]
                vv = np.r_[vv, s2.y[1][1:]]
            t_all.append(tt); iL_all.append(ii); vC_all.append(vv)
            q_all.append(np.full_like(tt, q))
            t, iL, vC = tt[-1], ii[-1], vv[-1]
            t = t1
    t = np.concatenate(t_all); iL = np.concatenate(iL_all)
    vC = np.concatenate(vC_all); q = np.concatenate(q_all)
    R = np.where(t < T_STEP, R1, R2)
    vo = (vC + p.rC * iL) / (1 + p.rC / R)
    return dict(t=t, iL=iL, vC=vC, vo=vo, q=q, R=R)


def window_metrics(s, p: P, t0, t1, n_last=10):
    m = (s["t"] >= t0) & (s["t"] <= t1)
    t, iL, vo, q, R = (s[k][m] for k in ("t", "iL", "vo", "q", "R"))
    # mean over an integer number of periods: trapezoid on non-uniform grid
    T = t[-1] - t[0]
    avg = lambda y: np.trapezoid(y, t) / T
    vo_m, io_m = avg(vo), avg(vo / R)
    pin, pout = avg(VIN * q * iL), avg(vo ** 2 / R)
    ml = t >= t1 - n_last * TS
    return dict(vo_mean=vo_m, io_mean=io_m,
                dvo_pp=np.ptp(vo[ml]), diL_pp=np.ptp(iL[ml]), iL_min=iL[ml].min(),
                iL_max=iL[ml].max(), Pin=pin, Pout=pout, eta=pout / pin)


def D_loss(p: P, Io: float):
    return (VO_REF + p.VF + Io * p.rL) / (VIN + p.VF - Io * p.rS)


def vo_dc_ccm(p: P, D, R):
    return (D * VIN - (1 - D) * p.VF) / (1 + (D * p.rS + p.rL) / R)


def report(name, p, D):
    s = simulate(p, D)
    print(f"\n=== {name}: L={p.L*1e6:.0f}uH C={p.C*1e6:.0f}uF rS={p.rS} rL={p.rL} rC={p.rC} VF={p.VF} D={D:.4f}")
    print(" analytic vo(12ohm)=%.3f  vo(6ohm)=%.3f" % (vo_dc_ccm(p, D, R1), vo_dc_ccm(p, D, R2)))
    for lab, (a, b) in {"R=12 (30-40ms)": (30e-3, 40e-3), "R=6 (90-100ms)": (90e-3, 100e-3)}.items():
        r = window_metrics(s, p, a, b)
        print(f" {lab}: " + ", ".join(f"{k}={v:.4g}" for k, v in r.items()))
    # transients
    vo, t = s["vo"], s["t"]
    pre = (t > 49e-3) & (t < 50e-3)
    post = t >= 50e-3
    v_post = vo[post]
    r6 = window_metrics(s, p, 90e-3, 100e-3)["vo_mean"]
    band = 0.01 * r6
    out = np.where(np.abs(vo[post] - r6) > band)[0]
    ts_settle = (t[post][out[-1]] - 50e-3) if len(out) else 0.0
    print(f" step: vo_min={v_post.min():.3f} V (dev {v_post.min()-r6:+.3f} V), settle(1%)={ts_settle*1e3:.2f} ms, "
          f"iL_max after step={s['iL'][post].max():.3f} A")
    st = t < 20e-3
    print(f" startup: iL_max={s['iL'][st].max():.3f} A, vo_max={vo[st].max():.3f} V")
    return s


if __name__ == "__main__":
    ideal = P(L=1e-3, C=100e-6)
    report("A ideal", ideal, 0.5)
    report("A ideal (start-file L=470u,C=22u)", P(L=470e-6, C=22e-6), 0.5)
    didact = P(L=1e-3, C=100e-6, rS=0.05, rL=0.1, rC=0.1, VF=0.5)
    Dd = D_loss(didact, 2.0)
    report("B didactic losses", didact, Dd)
    comm = P(L=1e-3, C=100e-6, rS=0.020, rL=0.195, rC=0.130, VF=0.525)
    Dc = D_loss(comm, 2.0)
    report("C commercial", comm, Dc)
