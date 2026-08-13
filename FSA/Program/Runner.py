import FSA.Program.Organizer as org
from typing import Literal

class Run_Buckling:
    def __init__(self):
        self.step1 = None
        self.factors = None

    def FSA(self, analysis_case:Literal['BENDING', 'AXIAL']):
        self.step1 = org.Buckle(selected_unit=org.select_unit, section=org.sec, material=org.mat, case=analysis_case)
        self.factors = self.step1.values
        modes_total = len(self.step1.values)
        print(f'modes : {modes_total}')

