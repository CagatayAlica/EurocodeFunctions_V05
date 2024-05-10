import math
import Section.EffectiveProp as eff
import Constants.Constants as cons
import Definitions.Definitions as defin


"""
EN 1993-1-1 Section 6.2 Resistance of Cross-Section
"""


class Sec6_2_3:
    """
    Section 6.2.3 Tension
    """

    def __init__(self, Anet: float):
        self.NplRd = defin.gross.Ar * defin.steel.fy / cons.gamma0
        self.NuRd = 0.90 * Anet * defin.steel.fu / cons.gamma2
        self.NtRd = min(self.NuRd, self.NplRd)


class Sec6_2_4:
    """
    Section 6.2.4 Compression
    """

    def __init__(self):
        self.NcRd = eff.Effective().Aeff * defin.steel.fy / cons.gamma0


class Sec6_2_5:
    """
    Section 6.2.5 Bending Moment
    """

    def __init__(self):
        self.McRdx = eff.Effective().Weffx * defin.steel.fy / cons.gamma0
        self.McRdy = eff.Effective().Weffy * defin.steel.fy / cons.gamma0


class Sec6_2_6:
    """
    Section 6.2.6 Shear
    """

    def __init__(self):
        self.Av = defin.section.a * defin.section.thk
        self.VplRd = self.Av*(defin.steel.fy/math.sqrt(3)) / cons.gamma0
