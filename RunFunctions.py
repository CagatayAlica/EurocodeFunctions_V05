import EffectiveSection.Modes.AxialCompression as Ax
import EffectiveSection.Modes.BendingStrong as Ben
import EffectiveSection.Modes.BendingWeakWeb as Benweb
import EffectiveSection.Modes.BendingWeakLip as Benlip
import Definitions.Definitions as defin
import Constants.Constants as cons
import Resistance.EN1993_1_1.Resistance as Resist
import Resistance.EN1993_1_3.Buckling as Buckle


print(f'{cons.secDivider}\nGross Cross Section Properties\n{cons.secDivider}')
print(
    f'Section : C{defin.section.A} x {defin.section.B} x {defin.section.C} - {defin.section.thk} / Fy: {defin.steel.fy} MPa\n'
    f'   Units : mm')
# input dictionary
input_dict = defin.gross.prop
# printing using For Loop
for key, value in input_dict.items():
    print(f"   {key}: {value:.2f}")

print(f'{cons.secDivider}\nEffective Cross Section Properties\n{cons.secDivider}')
ScomEd = Ax.ax.scomed
Aeff = Ax.ax.Axial_Aeff
ex = Ax.ax.Axial_dxgc
print(f'Effective cross section area under compression:\n   Aeff = {Aeff:.2f} mm2 for stress level {ScomEd:.2f} MPa\n'
      f'   enx = {ex:.2f} mm')
Ieff = Ben.Bending_strong.BendStrong_Ixeff
Weff = Ben.Bending_strong.BendStrong_Wxeff
print(f'Effective moment of inertia under bending about strong axis:\n   Ieff = {Ieff:.4f} mm3')
print(f'Effective section modulus under bending about strong axis:\n   Weff = {Weff:.4f} mm3')
IeffyLip = Benlip.Bending_weak_lip.BendWeakLip_Iyeff
WeffyLip = Benlip.Bending_weak_lip.BendWeakLip_Wyeff
print(f'Effective moment of inertia under bending about weak axis:\nLips are under compression\n   IeffyLip = {IeffyLip:.4f} mm3')
print(f'Effective section modulus under bending about weak axis:\nLips are under compression\n   WeffyLip = {WeffyLip:.4f} mm3')
IeffyWeb = Benweb.Bending_weak_web.BendWeakWeb_Iyeff
WeffyWeb = Benweb.Bending_weak_web.BendWeakWeb_Wyeff
print(f'Effective moment of inertia under bending about weak axis:\nWeb is under compression\n   IeffyWeb = {IeffyWeb:.4f} mm3')
print(f'Effective section modulus under bending about wak axis:\nWeb is under compression\n   WeffyWeb = {WeffyWeb:.4f} mm3')

print(Resist.ResistanceReport)
print(Buckle.BuckleReport)
