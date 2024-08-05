import math
import EffectiveSection.Modes.AxialCompression as Ax
import EffectiveSection.Modes.BendingStrong as Ben
import EffectiveSection.Modes.BendingWeakWeb as Benweb
import EffectiveSection.Modes.BendingWeakLip as Benlip
import Constants.Constants as cons
import Definitions.Definitions as defin


class Sec6_1_3:
    """
    Section 6.2.3 Tension
    """

    def __init__(self, Anet: float):
        self.NplRd = defin.gross.Ar * defin.steel.fy / cons.gamma0
        self.NuRd = 0.90 * Anet * defin.steel.fu / cons.gamma2
        self.NtRd = min(self.NuRd, self.NplRd)


class Sec6_1_4:
    """
    Section 6.2.4 Compression
    """

    def __init__(self):
        self.Aeff = Ax.ax.Axial_Aeff
        self.NcRd = self.Aeff * defin.steel.fy / cons.gamma0


class Sec6_2_5:
    """
    Section 6.2.5 Bending Moment
    """

    def __init__(self):
        self.Wxeff = Ben.Bending_strong.BendStrong_Wxeff
        self.WeffyLip = Benlip.Bending_weak_lip.BendWeakLip_Wyeff
        self.WeffyWeb = Benweb.Bending_weak_web.BendWeakWeb_Wyeff
        self.McRdx = self.Wxeff * defin.steel.fy / cons.gamma0
        self.McRdyLip = self.WeffyLip * defin.steel.fy / cons.gamma0
        self.McRdyWeb = self.WeffyWeb * defin.steel.fy / cons.gamma0


class Sec6_1_5:
    """
    Section 6.2.6 Shear
    """

    def __init__(self):
        self.fbv = None
        self.lambdaW = None
        self.VbRdz = self.ShearStrong()
        self.VbRdy = self.ShearWeak()

    def ShearStrong(self):
        # EN 1993-1-3 Eq 6.10
        self.lambdaW = 0.346 * defin.section.a / defin.section.thk * math.sqrt(defin.steel.fy / defin.steel.E)
        # EN 1993-1-3 Table 6.1
        if self.lambdaW <= 0.83:
            self.fbv = 0.58 * defin.steel.fy
        elif 0.83 < self.lambdaW < 1.40:
            self.fbv = 0.48 * defin.steel.fy / self.lambdaW
        else:
            self.fbv = 0.67 * defin.steel.fy / math.pow(self.lambdaW, 2)
        # EN 1993-1-1 Eq 6.18
        VRd = defin.section.a * defin.section.thk * self.fbv / cons.gamma0
        return VRd

    def ShearWeak(self):
        VRd = 2 * defin.section.b * defin.section.thk * defin.steel.fy / (math.sqrt(3) * cons.gamma0)
        return VRd


class StrengthReport:
    def __init__(self):
        Rep = f'{cons.secDivider}\nSECTION RESISTANCE\n{cons.secDivider}\n'
        Rep += f'Axial Tension Resistance / EN 1993-1-3 6.1.2:\n'
        Rep += f'   Ag = {defin.gross.Ar:.2f} mm2\n'
        Rep += f'   fy = {defin.steel.fy:.2f} MPa\n'
        Rep += f'   fu = {defin.steel.fu:.2f} MPa\n'
        Rep += f'   NtRd = {Sec6_1_3(defin.gross.Ar).NtRd / 1000:.2f} kN.\n'
        Rep += f'Axial Compression Resistance / EN 1993-1-3 6.1.3:\n'
        Rep += f'   Aeff = {Sec6_1_4().Aeff:.2f} mm2\n'
        Rep += f'   fy = {defin.steel.fy:.2f} MPa\n'
        Rep += f'   NcRd = {Sec6_1_4().NcRd / 1000:.2f} kN.\n'
        Rep += f'Bending Resistance About Strong Axis / EN 1993-1-3 6.1.4.1:\n'
        Rep += f'   Weffx = {Sec6_2_5().Wxeff:.2f} mm2\n'
        Rep += f'   McRdx = {Sec6_2_5().McRdx / 1000000:.2f} kNm.\n'
        Rep += f'Bending Resistance About Weak Axis and Web is Under Compression / EN 1993-1-3 6.1.4.1:\n'
        Rep += f'   Weffy = {Sec6_2_5().WeffyWeb:.2f} mm2\n'
        Rep += f'   McRdyWeb = {Sec6_2_5().McRdyWeb / 1000000:.2f} kNm.\n'
        Rep += f'Bending Resistance About Weak Axis and Lips are Under Compression / EN 1993-1-3 6.1.4.1:\n'
        Rep += f'   Weffy = {Sec6_2_5().WeffyLip:.2f} mm2\n'
        Rep += f'   McRdyLip = {Sec6_2_5().McRdyLip / 1000000:.2f} kNm.\n'
        Rep += f'Shear Resistance Along Web / EN 1993-1-3 6.1.5:\n'
        Rep += f'   LambdaW = {Sec6_1_5().lambdaW:.2f}\n'
        Rep += f'   fbv = {Sec6_1_5().fbv:.2f} MPa\n'
        Rep += f'   sw = {defin.section.a:.2f} mm\n'
        Rep += f'   t = {defin.section.thk:.2f} mm\n'
        Rep += f'   VbRdz = {Sec6_1_5().VbRdz / 1000:.2f} kN.\n'
        Rep += f'Shear Resistance Along Flanges / EN 1993-1-1 6.2.6:\n'
        Rep += f'   fbv = {defin.steel.fy:.2f} MPa\n'
        Rep += f'   sw = {defin.section.b:.2f} mm\n'
        Rep += f'   VbRdz = {Sec6_1_5().VbRdy / 1000:.2f} kN.'
        self.Report = Rep


ResistanceReport = StrengthReport().Report

