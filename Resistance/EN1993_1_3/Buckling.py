import math
import Constants.Constants as cons
import Definitions.Definitions as defin
import EffectiveSection.Modes.AxialCompression as Ax
import EffectiveSection.Modes.BendingStrong as Ben


class Sec6_2_1:
    def __init__(self):
        self.Aeff = Ax.ax.Axial_Aeff
        self.Ag = defin.gross.Ar
        self.imp = cons.bucklingcurve('b')
        self.lambda1 = 93.9 * cons.eps
        self.lambdabarX = self.slendernessFlex(defin.inp.Lx, math.sqrt(defin.gross.Ix / defin.gross.Ar))
        self.lambdabarY = self.slendernessFlex(defin.inp.Ly, math.sqrt(defin.gross.Iy / defin.gross.Ar))
        self.NcrFlexX = self.NcrFlex(defin.gross.Ix, defin.inp.Lx)
        self.NcrFlexY = self.NcrFlex(defin.gross.Iy, defin.inp.Ly)
        self.NcrT = self.NcrTorsional(defin.inp.Lt)
        self.lambdabarTor = self.slendernessTor(self.Aeff, defin.steel.fy, self.NcrT)
        self.ffX = self.calc_ksi(self.lambdabarX)[1]
        self.ffY = self.calc_ksi(self.lambdabarY)[1]
        self.ffT = self.calc_ksi(self.lambdabarTor)[1]
        self.ksiX = self.calc_ksi(self.lambdabarX)[0]
        self.ksiY = self.calc_ksi(self.lambdabarY)[0]
        self.ksiT = self.calc_ksi(self.lambdabarTor)[0]
        self.NbRd = self.calc_Nb()

    def slendernessFlex(self, Lcr, i):
        lambdabar = (Lcr / i) * (math.sqrt(self.Aeff / self.Ag) / self.lambda1)
        return lambdabar

    def NcrFlex(self, I, L):
        Ncr = math.pow(math.pi, 2) * defin.steel.E * I / math.pow(L, 2)
        return Ncr

    def NcrTorsional(self, Lt):
        """
        EN 1993-1-3 Equation Eq. 6.33
        :param Lt: is the buckling length of the member for torsional buckling. [mm]
        :return: The elastic critical torsional buckling force. [N]
        """
        ix2 = math.pow(math.sqrt(defin.gross.Ix / defin.gross.Ar), 2)
        iy2 = math.pow(math.sqrt(defin.gross.Iy / defin.gross.Ar), 2)
        yo2 = 0  # Symmetrical on y-y axis
        xo2 = math.pow(defin.gross.xo, 2)
        io2 = ix2 + iy2 + yo2 + xo2
        Ncrit = (1.0 / io2) * (
                defin.steel.G * defin.gross.It + (math.pow(math.pi, 2) * defin.steel.E * defin.gross.Cw) / math.pow(Lt,
                                                                                                                    2))
        return Ncrit

    def slendernessTor(self, Aeff, fy, NcrT):
        lambdaTor = math.sqrt(Aeff * fy / NcrT)
        return lambdaTor

    def calc_ksi(self, lam):
        ff = 0.5 * (1 + self.imp * (lam - 0.2) + math.pow(lam, 2))
        ksi = 1 / (ff + math.sqrt(math.pow(ff, 2) - math.pow(lam, 2)))
        if ksi >= 1.0:
            ksi = 1.0
        return ksi, ff

    def calc_Nb(self):
        Nb = min(self.ksiX, self.ksiY, self.ksiT) * self.Aeff * defin.steel.fy / cons.gamma0
        return Nb


class Sec6_3_2:
    def __init__(self):
        self.imp = cons.bucklingcurve('b')
        self.weff = Ben.Bending_strong.BendStrong_Wxeff
        self.Mcr = self.Critical_Moment(defin.inp.Ly)
        self.lambdaLTB = self.slendernessLTB(self.weff, self.Mcr)
        self.ksi = self.calc_ksi(self.lambdaLTB)
        self.MbRd = self.calc_Mb()

    def Critical_Moment(self, Lcr):
        C1 = defin.inp.C1
        pi2 = math.pow(math.pi, 2)
        E = defin.steel.E
        Iz = defin.gross.Iy
        Iw = defin.gross.Cw
        G = defin.steel.G
        It = defin.gross.It
        L2 = math.pow(Lcr, 2)
        Mcr = (C1 * pi2 * E * Iz / L2) * math.sqrt((Iw / Iz) + ((L2 * G * It) / (pi2 * E * Iz)))
        return Mcr

    def slendernessLTB(self, Weff, Mcr):
        lam = math.sqrt(Weff * defin.steel.fy / Mcr)
        return lam

    def calc_ksi(self, lam):
        ff = 0.5 * (1 + self.imp * (lam - 0.2) + math.pow(lam, 2))
        ksi = 1 / (ff + math.sqrt(math.pow(ff, 2) - math.pow(lam, 2)))
        if ksi >= 1.0:
            ksi = 1.0
        return ksi

    def calc_Mb(self):
        Nb = self.ksi * self.weff * defin.steel.fy / cons.gamma0
        return Nb


class BucklingReport:
    def __init__(self):
        Rep = f'{cons.secDivider}\nBUCKLING RESISTANCE\n{cons.secDivider}\n'
        Rep += f'Buckling Resistance in Axial Compression / EN 1993-1-1 6.3.1:\n'
        Rep += f'   alfa = {Sec6_2_1().imp:.2f}.\n'
        Rep += f'   Aeff = {Sec6_2_1().Aeff:.2f} mm2.\n'
        Rep += f'   fy = {defin.steel.fy:.2f} MPa.\n'
        Rep += f'   NcrX = {Sec6_2_1().NcrFlexX:.2f} N.\n'
        Rep += f'   NcrY = {Sec6_2_1().NcrFlexY:.2f} N.\n'
        Rep += f'   NcrTor = {Sec6_2_1().NcrT:.2f} N.\n'
        Rep += f'   lamX = {Sec6_2_1().lambdabarX:.2f}\n'
        Rep += f'   lamY = {Sec6_2_1().lambdabarY:.2f}\n'
        Rep += f'   lamTor = {Sec6_2_1().lambdabarTor:.2f}\n'
        Rep += f'   ffX = {Sec6_2_1().ffX:.2f}.\n'
        Rep += f'   ffY = {Sec6_2_1().ffY:.2f}.\n'
        Rep += f'   ffT = {Sec6_2_1().ffT:.2f}.\n'
        Rep += f'   ksiX = {Sec6_2_1().ksiX:.2f}.\n'
        Rep += f'   ksiY = {Sec6_2_1().ksiY:.2f}.\n'
        Rep += f'   ksiT = {Sec6_2_1().ksiT:.2f}.\n'
        Rep += f'   NbRd = {Sec6_2_1().NbRd / 1000:.2f} kN.\n'
        Rep += f'Buckling Resistance in Bending About Strong Axis / EN 1993-1-1 6.3.1:\n'
        Rep += f'   Weffx = {Sec6_3_2().weff:.2f} mm3.\n'
        Rep += f'   Mcr = {Sec6_3_2().Mcr:.2f} Nmm.\n'
        Rep += f'   lam = {Sec6_3_2().lambdaLTB:.2f}\n'
        Rep += f'   ksiLTB = {Sec6_3_2().ksi:.2f}.\n'
        Rep += f'   MbRdx = {Sec6_3_2().MbRd / 1000000:.2f} kNm.\n'

        self.Report = Rep


BuckleReport = BucklingReport().Report
