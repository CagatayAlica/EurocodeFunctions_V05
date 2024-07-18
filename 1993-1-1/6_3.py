import math
import Section.EffectiveProp as eff
import Constants.Constants as cons
import Definitions.Definitions as defin

"""
EN 1993-1-1 Section 6.3 Buckling Resistance of Members
"""


class Sec6_3_1_1:
    """
    Section 6.3.1.1 Buckling resistance
    """

    def __init__(self, ksi: float):
        self.ksi = ksi
        self.NbRd = self.ksi * eff.Effective().Aeff * defin.steel.fy / cons.gamma1


class Sec6_3_1_2:
    """
    Section 6.3.1.2 Buckling Curves
    """

    def __init__(self, lambda_bar: float):
        # Eq. 6.49
        self.ff = Eq6_49(lambda_bar)[0]
        # Reduction factor
        self.ksi = Eq6_49(lambda_bar)[1]


class Sec6_3_1_3:
    """
    Section 6.3.1.3 Slenderness for Flexural Buckling
    """

    def __init__(self):
        # Radius of gyration
        self.ix = defin.gross.Ix / defin.gross.Ar
        self.iy = defin.gross.Iy / defin.gross.Ar
        # Eq. 6.51
        self.Qa = math.sqrt(eff.Effective().Aeff / defin.gross.Ar)
        self.lambda_bar_x = (mem.lengths().Lx / self.ix) * (self.Qa / cons.lambda1)
        self.lambda_bar_y = (mem.lengths().Ly / self.iy) * (self.Qa / cons.lambda1)
        self.lambda_bar = max(self.lambda_bar_y, self.lambda_bar_x)


class Sec6_3_1_4:
    """
    Section 6.3.1.4 Slenderness for Torsional and Torsional-Flexural Buckling
    """

    def __init__(self):
        self.lambda_bar_t = math.sqrt(eff.Effective().Aeff * defin.steel.fy) / NcrT()


class Sec6_3_2_2:
    """
    Section 6.3.2.2 Lateral Torsional Buckling Curves
    """

    def __init__(self):
        self.lambda_bar_LT = math.sqrt(defin.gross.Wx * defin.steel.fy / Mcr())


# ======================================================================================================================
# Required Functions
# ======================================================================================================================
def NcrT():
    ix = defin.gross.Ix / defin.gross.Ar
    iy = defin.gross.Iy / defin.gross.Ar
    i02 = math.pow(ix, 2) + math.pow(iy, 2) + math.pow(defin.gross.xsc, 2) + math.pow(defin.gross.ysc, 2)
    NcrT = 1 / i02 * (
            defin.steel.G * defin.gross.It + (math.pow(cons.pi, 2) * defin.steel.E * defin.gross.Cw) / math.pow(
        mem.lengths().Lt, 2))
    return NcrT


def Mcr():
    Mcr = mem.lengths().C1 * math.pow(cons.pi, 2) * defin.steel.E * defin.gross.Iy / math.pow(mem.lengths().Lx,
                                                                                              2) * math.sqrt(
        defin.gross.Cw / defin.gross.Iy + (math.pow(mem.lengths().Lx, 2) * defin.steel.G * defin.gross.It) / (
                math.pow(cons.pi, 2) * defin.gross.E * defin.gross.Iy))
    return Mcr


def Eq6_49(lambda_bar: float):
    ff = 0.5 * (1 + cons.bucklingcurve('b') * (lambda_bar - 0.2) + math.pow(lambda_bar, 2))
    ksi = 1 / (ff + math.sqrt(math.pow(ff, 2) - math.pow(lambda_bar, 2)))
    if ksi > 1.0: ksi = 1.0
    return ff, ksi
