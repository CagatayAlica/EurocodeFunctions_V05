import math
import Resistance.EN1993_1_1.Resistance as Resist
import Resistance.EN1993_1_3.Buckling as Buckle
import Constants.Constants as cons



class SolveStuds:
    def __init__(self):
        self.Report = None
        self.Comb = 'Eurocode'
        # ==== Wind forces
        self.qw = 0.934  # kPa
        self.stud_int = 610.0  # mm
        self.height = 2800.0  # mm
        self.qww = self.qw * self.stud_int / 1000.0
        # ==== Loads
        self.Ned = -22.56 / 2.0  # kN
        self.Medx = self.qww * math.pow(self.height / 1000.0, 2) / 8.0 / 2.0  # kN.m
        self.Medy = 0.0  # kN.m
        self.Vedy = self.qww * (self.height / 1000.0) / 2.0 / 2.0  # kN
        self.Vedx = 0.0  # kN
        # ==== Resistance
        self.NtRd = Resist.Tension.NtRd
        self.NcRd = Resist.Compression.NcRd
        self.McRdx = Resist.Bending.McRdx
        self.McRdyLip = Resist.Bending.McRdyLip
        self.McRdWeb = Resist.Bending.McRdyWeb
        self.VbRdy = Resist.Shear.VbRdz
        self.VbRdx = Resist.Shear.VbRdy
        # ==== Buckling
        self.NbRd = Buckle.N_Resist.NbRd
        self.MbRd = Buckle.M_Resist.MbRd

        Rep = f'{cons.secDivider}\nDESIGN LOADS\n{cons.secDivider}\n'
        Rep += f'{self.Ned:.2f} kN, Axial force.\n'
        Rep += f'{self.Medx:.2f} kN.m, Bending moment about strong axis.\n'
        Rep += f'{self.Medy:.2f} kN.m, Bending moment about weak axis.\n'
        Rep += f'{self.Vedy:.2f} kN, Shear force on strong axis.\n'
        Rep += f'{self.Vedx:.2f} kN, Shear force on weak axis.\n'
        Rep += f'{cons.secDivider}\nULTIMATE LIMITS\n{cons.secDivider}\n'
        Rep += f'{self.NtRd/1000.0:.2f} kN, Tension resistance.\n'
        Rep += f'{self.NcRd/1000.0:.2f} kN, Compression resistance.\n'
        Rep += f'{self.McRdx/1000000.0:.2f} kN.m, Bending resistance about strong axis.\n'
        Rep += f'{self.McRdyLip/1000000.0:.2f} kN.m, Bending resistance about weak axis and lips are under compression.\n'
        Rep += f'{self.McRdWeb/1000000.0:.2f} kN.m, Bending resistance about weak axis and web is under compression.\n'
        Rep += f'{self.VbRdy/1000.0:.2f} kN, Shear resistance on strong axis.\n'
        Rep += f'{self.VbRdx/1000.0:.2f} kN, Shear resistance on weak axis.\n'
        Rep += f'{self.NbRd/1000.0:.2f} kN, Buckling resistance for axial compression.\n'
        Rep += f'{self.MbRd/1000000.0:.2f} kN.m, Buckling resistance for flexural.\n'




        self.Report = Rep

#Stud_1 = SolveStuds()

#Check = Capa.CheckCapacities(Stud_1.Comb,Stud_1.Ned,Stud_1.Medx,Stud_1.Vedy,Stud_1.Medy,Stud_1.Vedx)

#print(Stud_1.Report)

def checkStud(NcRd, McRdx, McRdy, NbRd, MbRd, Ned, ex, Med):
    # check strength
    ratio1 = (Ned/NcRd)+(Med/McRdx)+(ex/1000*Ned/McRdy)
    ratio2 = math.pow(Ned/NbRd, 0.8)+math.pow(Med/MbRd, 0.8)
    ratio = min(ratio1, ratio2)
    return ratio
snowDominant = checkStud(Resist.Compression.NcRd/1000.0,
          Resist.Bending.McRdx/1000000.0,
          Resist.Bending.McRdyLip/1000000.0,
          Buckle.N_Resist.NbRd/1000.0,
          Buckle.M_Resist.MbRd/1000000.0,
          12.07,
          2.11,
          0.41)
print(f'Stud Ratio = {snowDominant}')

windDominant = checkStud(Resist.Compression.NcRd/1000.0,
          Resist.Bending.McRdx/1000000.0,
          Resist.Bending.McRdyLip/1000000.0,
          Buckle.N_Resist.NbRd/1000.0,
          Buckle.M_Resist.MbRd/1000000.0,
          11.66,
          2.11,
          0.89)
print(f'Stud Ratio = {windDominant}')