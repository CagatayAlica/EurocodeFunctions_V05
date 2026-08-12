import math
import Constants.Constants as cons
import Definitions.Definitions as defin

# ==================================================================
# SCREWS LOADED IN SHEAR / EN 1993-1-3 Table 8.2
# ==================================================================
# ==== Inputs ====
t1 = defin.section.thk  # mm / The thickness of the thicker connected part or sheet.
t = defin.section.thk  # mm / The thinner of the thicker connected part or sheet.
Ag = defin.gross.Ar  # mm2 / Gross cross section area.
d = 5.5  # mm / The nominal diameter of the fastener.
dw = 12.0  # mm / The diameter of the screw head.
fu = defin.steel.fu  # MPa / Ultimate stress of the steel.
gM2 = cons.gamma2  # Partial factor.
nScrew = 14  # Quantity of the screws in total for single joint.
FvRk = 4.50  # kN / Shear resistance of single screw.
FtRd = 5.00  # kN / Tension resistance of single screw for 1.20 mm steel sheet.
FvEd = 7.5  # kN  / Design load.
FtEd = 0.00  # kN


# ==== Bearing resistance ====

def linearInterpolation(lowLimit, highLimit):
    y = lowLimit + ((0.5 - 0) * (highLimit - lowLimit)) / (1 - 0)
    return y


alfa = None
Rep = f'{cons.secDivider}\nSCREWS LOADED IN SHEAR / EN 1993-1-3 Table 8.2\n{cons.secDivider}\n'
Rep += f'==== Data Input ====\n'
Rep += f't1 = {t1:.2f} mm\nt = {t:.2f} mm\nd = {d:.2f} mm\nfu = {fu:.2f} MPa\ngM2 = {gM2:.2f}\nScrew Quantity = {nScrew}\n'
Rep += f'==== Bearing resistance ====\n'
if t == t1:
    alfa = 3.2 * math.sqrt(t / d)
    if alfa > 2.1: alfa = 2.1
    Rep += f't = t1 => Alfa = {alfa:.3f}\n'
elif t1 >= 2.5 and t < 1.0:
    alfa = 3.2 * math.sqrt(t / d)
    if alfa > 2.1: alfa = 2.1
    Rep += f't1 >= 2.5 and t < 1.0 => Alfa = {alfa:.3f}\n'
elif t1 >= 2.5 and t >= 1.0:
    alfa = 2.1
    Rep += f't1 >= 2.5 and t >= 1.0 => Alfa = {alfa:.3f}\n'
elif t < t1 < 2.5 * t:
    alfa = linearInterpolation(3.2 * math.sqrt(t / d), 2.1)
    Rep += f't < t1 < 2.5t => Alfa = {alfa:.3f}\n'

FbRd = alfa * fu * d * t / gM2
Rep += f'FbRd = {FbRd / 1000.:.3f} kN for single screw.\n'
Rep += f'ΣFbRd = {FbRd * nScrew / 1000.:.3f} kN for joint.\n'

# ==== Net-Section resistance ====
Rep += f'==== Net-Section resistance ====\n'
Anet = Ag - nScrew * d * t
Rep += f'Gross cross section area, Ag = {Ag:.2f} mm2\nNet cross section area, Anet = {Anet:.2f} mm2\n'
FnRd = Anet * fu / gM2
Rep += f'FnRd = {FnRd / 1000.0:.3f} kN for joint.\n'

# ==== Shear resistance ====
Rep += f'==== Shear resistance ====\n'
FvRd = FvRk / gM2
Rep += f'FvRd = {FvRd:.3f} kN for single screw\n'
Rep += f'ΣFvRd = {FvRd * nScrew:.3f} kN for joint.\n'

Rep += f'==== Result ====\n'
Rep += f'NOTE : Deformation is limited by ceiling panel by placing screws through them.\n'
FjRd = min(FbRd * nScrew / 1000., FnRd / 1000.0, FvRd * nScrew)
Rep += f'FjRd = {FjRd:.3f} kN\n'
RatShear = FvEd / FjRd
Rep += f'Capacity ratio is {FvEd:.3f} / {FjRd:.3f} = {RatShear:.3f}\n'


# ==================================================================
# SCREWS LOADED IN TENSION / EN 1993-1-3 Table 8.2
# ==================================================================
FpRd = FtRd / gM2
tFpRd = FpRd * nScrew
Rep += f'{cons.secDivider}\nSCREWS LOADED IN TENSION / EN 1993-1-3 Table 8.2\n{cons.secDivider}\n'
Rep += f'==== Pull-Through resistance ====\n'
Rep += f'FpRd = {FpRd:.3f} kN per screw.\n'
Rep += f'ΣFpRd = {tFpRd:.3f} kN per joint.\n'
RatTension = FtEd / tFpRd
Rep += f'Capacity ratio is {FtEd:.3f} / {tFpRd:.3f} = {RatTension:.3f}\n'

# ==================================================================
# Combıned Actıon Check
# ==================================================================
FpRd = FtRd / gM2
tFpRd = FpRd * nScrew
Rep += f'{cons.secDivider}\nSCREWS LOADED IN TENSION AND THE SHEAR\n{cons.secDivider}\n'
Rep += f'==== Combined Action ====\n'
Rep += f'Capacity Ratio for Shear = {RatShear:.3f}.\n'
Rep += f'Capacity Ratio for Tension = {RatTension:.3f}.\n'
RatComb = math.pow(RatTension, 0.8)+math.pow(RatShear, 0.8)
Rep += f'Combined Ratio = {RatShear:.3f}\u2070\u2078+{RatTension:.3f}\u2070\u2078 = {RatComb:.3f}'


print(Rep)
