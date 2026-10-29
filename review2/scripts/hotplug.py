# hot-plug: 5 V step through cable R+L into VBUS node -> D1 (Schottky) -> C_vsys; D4 TVS on VBUS (piecewise linear)
import numpy as np
from scipy.integrate import solve_ivp
def tvs(v, on):
    if not on: return 0.0
    # ESD5Z5.0: VBR >= 6.2 V @1 mA; VC 11.6 V typ @ 5 A, 18.6 V max @ 9.4 A (8/20). Typ model: knee 6.6 V, slope (11.6-6.6)/5 = 1.0 ohm
    return max(0.0, (v-6.6)/1.0)
def d1(v):  # DFLS130L forward: ~0.25 V knee + 0.08 ohm (approx 0.33 V at 1 A)
    return max(0.0, (v-0.25)/0.08)
def run(L, R, C, on, Cbus=0.2e-6):
    def f(t, y):
        i, vb, vs = y
        id1 = d1(vb-vs); it = tvs(vb, on)
        return [(5.0 - R*i - vb)/L, (i - id1 - it)/Cbus, (id1 - 0.05)/C]
    s = solve_ivp(f, [0, 40e-6], [0, 0, 0], max_step=2e-9, method='LSODA')
    return s.y[1].max(), s.y[2].max()
print('L uH, R ohm, C_eff uF : VBUS pk / VSYS pk  without D4  |  with D4')
for L in (0.5e-6, 1e-6, 1.5e-6):
    for R in (0.1, 0.2, 0.4):
        for C in (5e-6, 10.4e-6):
            a = run(L, R, C, False); b = run(L, R, C, True)
            print('%.1f %.1f %.1f : %.2f / %.2f  |  %.2f / %.2f' % (L*1e6, R, C*1e6, a[0], a[1], b[0], b[1]))

print('\nalternatives at the worst case L=1.5 uH, R=0.1, C_eff 5 uF (VSYS peak):')
import functools
def run2(L,R,C,tv, Cd=0, Rd=0):
    Cbus=0.2e-6
    def f(t,y):
        i,vb,vs,vd=y
        id1=d1(vb-vs); it=tv(vb); idmp=(vb-vd)/Rd if Cd else 0.0
        return [(5.0-R*i-vb)/L,(i-id1-it-idmp)/Cbus,(id1-0.05)/C,(idmp/Cd if Cd else 0.0)]
    s=solve_ivp(f,[0,40e-6],[0,0,0,0],max_step=2e-9,method='LSODA'); return s.y[2].max()
esd5z=lambda v: max(0.0,(v-6.6)/1.0)
smf=lambda v: max(0.0,(v-6.7)/0.06)     # SMF5.0A class: VBR 6.4-7.0, VC 9.2 V @ 43.5 A -> ~0.06 ohm
print(' ESD5Z5.0 (as built)        %.2f' % run2(1.5e-6,0.1,5e-6,esd5z))
print(' SMF5.0A-class TVS          %.2f' % run2(1.5e-6,0.1,5e-6,smf))
print(' ESD5Z + 10uF/1ohm damper   %.2f' % run2(1.5e-6,0.1,5e-6,esd5z,10e-6,1.0))
print(' ESD5Z + 4.7uF/1ohm damper  %.2f' % run2(1.5e-6,0.1,5e-6,esd5z,4.7e-6,1.0))
