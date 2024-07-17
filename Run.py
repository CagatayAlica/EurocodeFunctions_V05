import EffectiveSection.Modes.AxialCompression as Ax
import EffectiveSection.Modes.BendingStrong as Ben
import EffectiveSection.Modes.BendingWeakWeb as Benweb
import EffectiveSection.Modes.BendingWeakLip as Benlip
import Definitions.Definitions as defin
secDivider = '============================================'
print(f'{secDivider}\nEffective Cross Section Properties\n{secDivider}')
print(f'Section : C{defin.section.A}x{defin.section.B}x{defin.section.C}-{defin.section.thk} / Fy: {defin.steel.fy} MPa')
Igry = defin.gross.Ix
print(f'Gross section moment of inertia about strong axis:\nIgr: {Igry} mm3')
Igrz = defin.gross.Iy
print(f'Gross section moment of inertia about weak axis:\nIgr: {Igrz} mm3')
Aeff = Ax.ax.Axial_Aeff
print(f'Effective cross section area under compression:\nAeff = {Aeff} mm2')
Ieff = Ben.Bending_strong.BendStrong_Ixeff
Weff = Ben.Bending_strong.BendStrong_Wxeff
print(f'Effective moment of inertia under bending about strong axis:\nIeff: {Ieff} mm3')
print(f'Effective section modulus under bending about strong axis:\nWeff: {Weff} mm3')
IeffyLip = Benlip.Bending_weak_lip.BendWeakLip_Iyeff
WeffyLip = Benlip.Bending_weak_lip.BendWeakLip_Wyeff
print(f'Effective moment of inertia under bending about weak axis:\nIeffyLip: {IeffyLip} mm3')
print(f'Effective section modulus under bending about wak axis:\nWeffyLip: {WeffyLip} mm3')
IeffyWeb = Benweb.Bending_weak_web.BendWeakWeb_Iyeff
WeffyWeb = Benweb.Bending_weak_web.BendWeakWeb_Wyeff
print(f'Effective moment of inertia under bending about weak axis:\nIeffyWeb: {IeffyWeb} mm3')
print(f'Effective section modulus under bending about wak axis:\nWeffyWeb: {WeffyWeb} mm3')
