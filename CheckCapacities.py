import math
import Definitions.Definitions as defin
import Resistance.EN1993_1_1.Resistance as Resist
import Resistance.EN1993_1_3.Buckling as Buckle
import Constants.Constants as cons
import ElementTypes.Purlins as purlins


class CheckCapacities:
    def __init__(self, Comb, Ned, Medx, Vedy, Medy, Vedx):
        # ==== Loads ====
        # [Comb, N, Mx, Vy, My, Vx]
        Comb = Comb
        Ned = Ned
        Medx = Medx
        Vedy = Vedy
        Medy = Medy
        Vedx = Vedx

        # === Resistance ===
        NbRd = Buckle.N_Resist.NbRd / 1000.0
        MbRd = Buckle.M_Resist.MbRd / 1000000.0
        NtRd = Resist.Tension.NtRd / 1000.0
        NcRd = Resist.Compression.NcRd / 1000.0
        McRdx = Resist.Bending.McRdx / 1000000.0
        McRdyLip = Resist.Bending.McRdyLip / 1000000.0
        McRdyWeb = Resist.Bending.McRdyWeb / 1000000.0
        VcRdy = Resist.Shear.VbRdy / 1000.0  # Shear Resistance Along Flanges
        VcRdx = Resist.Shear.VbRdz / 1000.0  # Shear Resistance Along Web

        Ratio_List = {}

        Rep = f'{cons.secDivider}\nDESIGN LOADS for {Comb}\n{cons.secDivider}\n'
        if Ned >= 0.0:
            Rep += f'{cons.sp3}Ned = {Ned:.3f} kN. Axial tension.\n'
        else:
            Rep += f'{cons.sp3}Ned = {Ned:.3f} kN. Axial compression.\n'
        Rep += f'{cons.sp3}Medx = {Medx:.3f} kN.m\n'
        if Medy >= 0.0:
            Rep += f'{cons.sp3}Medy = {Medy:.3f} kN.m. Compression on web.\n'
        else:
            Rep += f'{cons.sp3}Medy = {Medy:.3f} kN.m. Compression on lips.\n'
        Rep += f'{cons.sp3}Vedx = {Vedx:.3f} kN. Shear along flanges.\n'
        Rep += f'{cons.sp3}Vedy = {Vedy:.3f} kN. Shear along web.\n'
        Rep += f'{cons.secDivider}\nMEMBER RESISTANCE\n{cons.secDivider}\n'
        Rep += f'{cons.sp3}NbRd = {NbRd:.3f} kN\n'
        Rep += f'{cons.sp3}MbRd = {MbRd:.3f} kN.m\n'
        Rep += f'{cons.sp3}NtRd = {NtRd:.3f} kN\n'
        Rep += f'{cons.sp3}NcRd = {NcRd:.3f} kN\n'
        Rep += f'{cons.sp3}McRdx = {McRdx:.3f} kN.m\n'
        Rep += f'{cons.sp3}McRdyWeb = {McRdyLip:.3f} kN.m\n'
        Rep += f'{cons.sp3}McRdyLip = {McRdyWeb:.3f} kN.m\n'
        Rep += f'{cons.sp3}VcRdx = {VcRdx:.3f} kN\n'
        Rep += f'{cons.sp3}VcRdy = {VcRdy:.3f} kN\n'

        isTension = True
        isCompOnWeb = True

        if Medy < 0.0:
            # + for compression on web
            isCompOnWeb = False
        else:
            isCompOnWeb = True

        Medy = abs(Medy)

        if Ned < 0.0:
            # compression
            isTension = False
            Ned = - Ned
        else:
            # tension
            isTension = True

        # Combined Tension and Bending EN 1993-1-3 6.1.8
        Rat_6_23 = None
        Rat_6_24 = None
        Rat_6_25 = None
        Rat_6_27 = None
        Rat_6_36 = None
        Rep += f'{cons.secDivider}\nCAPACITY CHECKS for {Comb}\n{cons.secDivider}\n'
        Rep += f'Eurocode 1993-1-3\n'
        if isTension:
            if isCompOnWeb:
                Rat_6_23 = (Ned / NtRd) + abs(Medx / McRdx) + abs(Medy / McRdyWeb)
                Rep += f'{cons.sp3}Equation 6.23: {Rat_6_23:.3f}\n'
                Rep += f'{cons.sp9}(Ned / NtRd) + (Medx / McRdx) + (Medy / McRdyWeb)\n'
                Rep += f'{cons.sp9}({Ned:.3f} / {NtRd:.3f}) + ({Medx:.3f} / {McRdx:.3f}) + ({Medy:.3f} / {McRdyWeb:.3f})\n'
            else:
                Rat_6_23 = (Ned / NtRd) + abs(Medx / McRdx) + abs(Medy / McRdyLip)
                Rep += f'{cons.sp3}Equation 6.23: {Rat_6_23:3f}\n'
                Rep += f'{cons.sp9}(Ned / NtRd) + (Medx / McRdx) + (Medy / McRdyLip)\n'
                Rep += f'{cons.sp9}({Ned:.3f} / {NtRd:.3f}) + ({Medx:.3f} / {McRdx:.3f}) + ({Medy:.3f} / {McRdyLip:.3f})\n'
        if isTension:
            if isCompOnWeb:
                Rat_6_24 = abs(Medx / McRdx) + abs(Medy / McRdyWeb) - (Ned / NtRd)
                Rep += f'{cons.sp3}Equation 6.24: {Rat_6_24:.3f}\n'
                Rep += f'{cons.sp9}(Medx / McRdx) + (Medy / McRdyWeb) - (Ned / NtRd)\n'
                Rep += f'{cons.sp9}({Medx:.3f} / {McRdx:.3f}) + ({Medy:.3f} / {McRdyWeb:.3f}) - ({Ned:.3f} / {NtRd:.3f})\n'
            else:
                Rat_6_24 = abs(Medx / McRdx) + abs(Medy / McRdyLip) - (Ned / NtRd)
                Rep += f'{cons.sp3}Equation 6.24: {Rat_6_24:.3f}\n'
                Rep += f'{cons.sp9}(Medx / McRdx) + (Medy / McRdyLip) - (Ned / NtRd)\n'
                Rep += f'{cons.sp9}({Medx:.3f} / {McRdx:.3f}) + ({Medy:.3f} / {McRdyLip:.3f}) - ({Ned:.3f} / {NtRd:.3f})\n'

        # Combined Compression and Bending EN 1993-1-3 6.1.9
        eny = Resist.Ax.ax.Axial_dxgc
        dMxed = Ned * (eny / 1000.0)
        dMyed = 0.0  # zero eccentricity

        if not isTension:
            if isCompOnWeb:
                Rat_6_25 = (Ned / NcRd) + (abs(Medx + dMxed) / McRdx) + ((Medy + dMyed) / McRdyWeb)
                Rep += f'{cons.sp3}Equation 6.25: {Rat_6_25:.3f}\n'
                Rep += f'{cons.sp9}(Ned / NcRd) + ((Medx + dMxed) / McRdx) + ((Medy + dMyed) / McRdyWeb)\n'
                Rep += f'{cons.sp9}({Ned:.3f} / {NcRd:.3f}) + (({Medx:.3f} + {dMxed:.3f}) / {McRdx:.3f}) + (({Medy:.3f} + {dMyed:.3f}) / {McRdyWeb:.3f})\n'
            else:
                Rat_6_25 = (Ned / NcRd) + (abs(Medx + dMxed) / McRdx) + ((Medy + dMyed) / McRdyLip)
                Rep += f'{cons.sp3}Equation 6.25: {Rat_6_25:.3f}\n'
                Rep += f'{cons.sp9}(Ned / NcRd) + ((Medx + dMxed) / McRdx) + ((Medy + dMyed) / McRdyLip)\n'
                Rep += f'{cons.sp9}({Ned:.3f} / {NcRd:.3f}) + (({Medx:.3f} + {dMxed:.3f}) / {McRdx:.3f}) + (({Medy:.3f} + {dMyed:.3f}) / {McRdyLip:.3f})\n'
        if isTension:
            if isCompOnWeb:
                Rat_6_25 = 'N/A, Ned is Tension.'
                Rep += f'{cons.sp3}Equation 6.25: {Rat_6_25}\n'

        # Combined Shear Force, Axial Force and Bending Moment
        if Vedy > 0.5 * VcRdy:
            # For simplicity MfRd / MplRd ratio is taken 0.
            if isTension:
                Rat_6_27 = (Ned / NtRd) + abs(Medx / McRdx) + math.pow(2 * Vedy / VcRdy - 1, 2)
                Rep += f'{cons.sp3}Equation 6.27: {Rat_6_27:.3f}\n'
                Rep += f'{cons.sp9}(Ned / NtRd) + (Medx / McRdx) + (2 * Vedy / VcRdy-1)\u00B2\n'
                Rep += f'{cons.sp9}({Ned:.3f} / {NtRd:.3f}) + ({Medx:.3f} / {McRdx:.3f}) + (2 x {Vedy:.3f} / {VcRdy:.3f} - 1)\u00B2\n'
            else:
                Rat_6_27 = (Ned / NcRd) + abs(Medx / McRdx) + math.pow(2 * Vedy / VcRdy - 1, 2)
                Rep += f'{cons.sp3}Equation 6.27: {Rat_6_27:.3f}\n'
                Rep += f'{cons.sp9}(Ned / NcRd) + (Medx / McRdx) + (2 x Vedy / VcRdy - 1)\u00B2\n'
                Rep += f'{cons.sp9}({Ned:.3f} / {NcRd:.3f}) + ({Medx:.3f} / {McRdx:.3f}) + (2 x {Vedy:.3f} / {VcRdy:.3f} - 1)\u00B2\n'
        else:
            Rat_6_27 = 'N/A, Ved < 0.5 x VcRdy.'
            Rep += f'{cons.sp3}Equation 6.27: {Rat_6_27}\n'
        # Combined Buckling
        if not isTension:
            Rat_6_36 = math.pow(Ned / NbRd, 0.8) + math.pow(abs(Medx) / MbRd, 0.8)
            Rep += f'{cons.sp3}Equation 6.36: {Rat_6_36:.3f}\n'
            Rep += f'{cons.sp9}(Ned / NbRd)\u2070\u2078 + (Medx / MbRd)\u2070\u2078\n{cons.sp9}({Ned:.2f} / {NbRd:.2f})\u2070\u2078 + ({Medx:.2f} / {MbRd:.2f})\u2070\u2078\n'
        else:
            Rat_6_36 = 'N/A, Ned is Tension.'
            Rep += f'{cons.sp3}Equation 6.36: {Rat_6_36}\n'
        Ratio_List.update({Comb: {"Eq 6.23": Rat_6_23,
                                  "Eq 6.24": Rat_6_24,
                                  "Eq 6.25": Rat_6_25,
                                  "Eq 6.27": Rat_6_27,
                                  "Eq 6.36": Rat_6_36}})
        print(Ratio_List)
        print(Rep)


#calc = purlins.SolvePurlins()
#for i in calc.Eds:
#    CheckCapacities(i[0], i[1], i[2], i[3], i[4], i[5])
