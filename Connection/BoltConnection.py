import math
import Constants.Constants as cons
import Definitions.Definitions as defin

e1 = 25.00
e2 = 25.00
Ag = defin.gross.Ar  # mm2 / Gross cross section area.
d = 12.00
d0 = 13.00
t = defin.section.thk  # mm / The thinner of the thicker connected part or sheet.
tp = 2.5
fu = defin.steel.fu  # MPa / Ultimate stress of the steel.
gM2 = cons.gamma2  # Partial factor.
num_bolt_x = 1
num_bolt_y = 1
Anet = Ag - (num_bolt_x * d0 * t)

if e1 / (3 * d) < 1.0:
    alfab = e1 / (3 * d)
else:
    alfab = 1.0

kt = None
if 0.75 <= t <= 1.25:
    kt = (0.8 * t + 1.5) / 2.5
elif t > 1.25:
    kt = 1.0

FbRd = 2.5 * alfab * kt * fu * d * t / gM2
FbRdp = 2.5 * alfab * kt * fu * d * tp / gM2
print(f'Bearing strength, FbRd:\nFor C profile :{FbRd * (num_bolt_x * num_bolt_y) * 2/1000.0:.3f} kN')
print(f'For gusset plate :{FbRdp * (num_bolt_x * num_bolt_y)*2/1000.0:.3f} kN')
r = num_bolt_x / (num_bolt_y * num_bolt_x)
u = 2 * e2
FnRd = (1 + 3 * r * (d0 / u - 0.3)) * Anet * fu / gM2
if FnRd>Anet*fu/gM2:
    FnRd = Anet*fu/gM2
print(f'Net section strength:\nFnRd = {FnRd/1000.0:.3f} kN')
