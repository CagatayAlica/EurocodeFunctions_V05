import math
import Definitions.Definitions as defin
from typing import Final, Literal

# Tolerance for each iteration
tol1000 = 1.0 / 1000.0
tol100 = 1.0 / 100.0
# pi 3.14
pi = math.pi
# factor depending on fy
eps = math.sqrt(235 / defin.steel.fy)
# slenderness value to determine the relative slenderness
lambda1 = pi * math.sqrt(defin.steel.E / defin.steel.fy)
# Partial factor
gamma0 = 1.00
gamma1 = 1.25
gamma2 = 1.25


# Table 6.1
def bucklingcurve(val):
    if val == 'a':
        alfa = 0.21
    elif val == 'b':
        alfa = 0.34
    elif val == 'c':
        alfa = 0.49
    else:
        alfa = 0.76
    return alfa


Mode = Literal['Compression', 'Bending', 'BendingMinorWeb', 'BendingMinorLip']
