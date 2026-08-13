from typing import Literal
from Section.Materials import material
from Section.CreateSections import C_Section
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
sec = C_Section(90, 45, 10, 1.2, 2.5, 270, mat)
print(sec)
# sec = Section.U_Section(defs.A,defs.B,defs.t,defs.R,0, mat)
# sec = Section.Omega_Section(100, 48,12,10,1,3,0,mat)


def main():
    """The main entry point function containing the core logic."""
    BucklingAnalysis = fsa.Run_Buckling()
    Buckle_Axial = BucklingAnalysis.FSA('AXIAL')
    Buckle_Bending = BucklingAnalysis.FSA('BENDING')


# The execution guard
if __name__ == "__main__":
    main()
