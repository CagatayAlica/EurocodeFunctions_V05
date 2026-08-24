from typing import Literal
import FSA.Program.Organizer as org
from Section.Materials import material


class Run_Buckling:
    def __init__(self, section, material, unit):
        """
        Accepts section, material, and unit during initialization.
        """
        self.sec = section
        self.mat = material
        self.unit = unit
        self.step1 = None
        self.factors = None

    def FSA(self, analysis_case: Literal['BENDING', 'AXIAL']):
        # Use the stored properties
        self.step1 = org.Buckle(
            selected_unit=self.unit,
            section=self.sec,
            material=self.mat,
            case=analysis_case
        )
        self.factors = self.step1.values
        print(self.factors)
        modes_total = len(self.step1.values)
        print(f'Modes ({analysis_case}): {modes_total}')

        return self.factors
