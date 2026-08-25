from typing import Literal
from Section.Materials import material
from Section.CreateSections import C_Section, U_Section
import FSA.Program.Runner as fsa
from EffectiveSection.Modes import AxialCompression, BendingStrong, BendingWeakLip, BendingWeakWeb


class Unit:
    def __init__(self, unit: Literal['METRIC','IMPERIAL']):
        """
        General selection of units.
        Metric for length in mm, stress in MPa.
        Imperial for length in inches, stress in ksi.
        :param unit: Select METRIC or IMPERIAL
        """
        self.unit = unit
        self.name = None
        if self.unit == 'METRIC':
            self.name = '[mm, MPa]'
            self.length_unit = 'mm'
            self.stress_unit = 'MPa'
            self.toInches = 1.0 / 25.4
            self.toKsi = 0.1450377377
        else:
            self.name = '[in, ksi]'
            self.length_unit = 'in'
            self.stress_unit = 'ksi'
            self.toInches = 1.0
            self.toKsi = 1.0

    def __str__(self):
        return f"Selected unit is {self.unit}, {self.name}"

# ======================================================================================================================
# Selection of unit
# ======================================================================================================================
select_unit = Unit('METRIC')
print(select_unit)
# ======================================================================================================================
# Steel material in selected unit
# ======================================================================================================================
mat = material('S350',350,420)
print(mat)
# ======================================================================================================================
# Defining the section in selected unit
# ======================================================================================================================
sec = C_Section(120, 50, 15, 1.5, 2.5, 270, mat)
print(sec)

def bucklingAnalysis():
    # 1. Instantiates section, material, and units ONCE in __init__
    BucklingAnalysis = fsa.Run_Buckling(sec, mat, select_unit)

    # 2. Runs FSA using the pre-initialized section and material
    Scr_axial = BucklingAnalysis.FSA('AXIAL')
    Scr_bending = BucklingAnalysis.FSA('BENDING')

    # Multiply index [2] of factors by material yield strength (fy)
    sigma_cr_axial = [row[2] * mat.fy for row in Scr_axial]
    sigma_cr_bending = [row[2] * mat.fy for row in Scr_bending]
    s = 0
    for i in sigma_cr_axial:
        Scr_axial[s].append(i)
        s = +1
    s = 0
    for y in sigma_cr_bending:
        Scr_bending[s].append(y)
        s = +1

    report = f'BUCKLING ANALYSIS REPORT\n________________\n'
    for i in Scr_axial:
        report += (f'Case \t: {i[0]}\n'
                   f'Buckling Mode \t: {i[1]}\n'
                   f'Critical buckling load factor \t: {i[2]:.3f}\n'
                   f'Critical buckling stress \t: {i[3]:.3f} MPa\n')
    for i in Scr_bending:
        report += (f'Case \t: {i[0]}\n'
                   f'Buckling Mode \t: {i[1]}\n'
                   f'Critical buckling load factor \t: {i[2]:.3f}\n'
                   f'Critical buckling stress \t: {i[3]:.3f} MPa\n')

    print(report)
    return Scr_axial, Scr_bending

BucklingResults = bucklingAnalysis()

def effective(res):
    f_crit_ax = None
    for group in res:
        for mode in group:
            if mode[0] == 'AXIAL' and mode[1] == 'distortional':
                f_crit_ax = mode[3]
                break

    if f_crit_ax is None:
        raise ValueError("f_crit is None. Ensure BucklingResults calculated a valid critical stress.")

    f_crit_bend = None
    for group in res:
        for mode in group:
            if mode[0] == 'BENDING' and mode[1] == 'distortional':
                f_crit_bend = mode[3]
                break

    if f_crit_bend is None:
        raise ValueError("f_crit is None. Ensure BucklingResults calculated a valid critical stress.")

    axialComp = AxialCompression.AxialComp(mat, sec, f_crit_ax)
    bending = None
    if sec.angle == 0:
        bending = BendingStrong.bendStrong(mat, sec, f_crit_bend)
    if sec.angle == 90:
        bending = BendingWeakWeb.bendWeakWeb(mat, sec, f_crit_bend)
    if sec.angle == 270:
        bending = BendingWeakLip.bendWeakLip(mat, sec, f_crit_bend)
    return f_crit_ax, axialComp, f_crit_bend, bending


def main():
    bucklingAnalysis()
    axial = effective(BucklingResults)[1]
    bending = effective(BucklingResults)[3]
    print(f'Aeff : {axial.Axial_Aeff}')
    print(f'Weff : {bending.Weff}')


if __name__ == "__main__":
    main()
