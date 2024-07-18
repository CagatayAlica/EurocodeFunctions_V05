import EffectiveSection.Modes.AxialCompression as Ax
import EffectiveSection.Modes.BendingStrong as Ben
import EffectiveSection.Modes.BendingWeakWeb as Benweb
import EffectiveSection.Modes.BendingWeakLip as Benlip
import Definitions.Definitions as defin
import Constants.Constants as cons

print(f'{cons.secDivider}\nGross Cross Section Properties\n{cons.secDivider}')
print(
    f'Section : C{defin.section.A} x {defin.section.B} x {defin.section.C} - {defin.section.thk} / Fy: {defin.steel.fy} MPa')
# input dictionary
input_dict = defin.gross.prop
# printing using For Loop
for key, value in input_dict.items():
    print(f"{key}: {value:.4f}")

print(f'{cons.secDivider}\nEffective Cross Section Properties\n{cons.secDivider}')
Aeff = Ax.ax.Axial_Aeff
print(f'Effective cross section area under compression:\nAeff = {Aeff:.2f} mm2')
Ieff = Ben.Bending_strong.BendStrong_Ixeff
Weff = Ben.Bending_strong.BendStrong_Wxeff
print(f'Effective moment of inertia under bending about strong axis:\nIeff: {Ieff:.4f} mm3')
print(f'Effective section modulus under bending about strong axis:\nWeff: {Weff:.4f} mm3')
IeffyLip = Benlip.Bending_weak_lip.BendWeakLip_Iyeff
WeffyLip = Benlip.Bending_weak_lip.BendWeakLip_Wyeff
print(f'Effective moment of inertia under bending about weak axis:\nIeffyLip: {IeffyLip:.4f} mm3')
print(f'Effective section modulus under bending about weak axis:\nWeffyLip: {WeffyLip:.4f} mm3')
IeffyWeb = Benweb.Bending_weak_web.BendWeakWeb_Iyeff
WeffyWeb = Benweb.Bending_weak_web.BendWeakWeb_Wyeff
print(f'Effective moment of inertia under bending about weak axis:\nIeffyWeb: {IeffyWeb:.4f} mm3')
print(f'Effective section modulus under bending about wak axis:\nWeffyWeb: {WeffyWeb:.4f} mm3')
