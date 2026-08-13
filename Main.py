from typing import Literal
from Section.Materials import material
from Section.CreateSections import C_Section, U_Section
import FSA.Program.Runner as fsa


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
sec = C_Section(140, 45, 10, 1.2, 2.5, 270, mat)
print(sec)


def main():
    # 1. Instantiates section, material, and units ONCE in __init__
    BucklingAnalysis = fsa.Run_Buckling(sec, mat, select_unit)

    # 2. Runs FSA using the pre-initialized section and material
    Scr_axial = BucklingAnalysis.FSA('AXIAL')
    Scr_bending = BucklingAnalysis.FSA('BENDING')

    # Multiply index [2] of factors by material yield strength (fy)
    sigma_cr_axial = [row[2] * mat.fy for row in Scr_axial]
    sigma_cr_bending = [row[2] * mat.fy for row in Scr_bending]
    s=0
    for i in sigma_cr_axial:
        Scr_axial[s].append(i)
        s=+1
    s=0
    for y in sigma_cr_bending:
        Scr_bending[s].append(y)
        s=+1

    print("Axial Critical Stresses:", sigma_cr_axial)
    print("Bending Critical Stresses:", sigma_cr_bending)
    print("Axial Critical Load Factor and stresses:", Scr_axial)
    print("Bending Critical Load Factor and stresses:", Scr_bending)


if __name__ == "__main__":
    main()
