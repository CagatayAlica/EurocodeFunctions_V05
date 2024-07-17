import math
import EffectiveSection.EN1993_1_5.Sec4 as Sec4
import EffectiveSection.EN1993_1_3.Sec5_5_3 as Sec553
import Definitions.Definitions as defin
import numpy as np
import matplotlib.pyplot as plt


def calcEffectiveProps(data: []):
    # data:
    # 0 id , 1 inodeX, 2 inodeY, 3 jnodeX, 4 JnodeY, 5 thickness
    # Area of cross-section parts
    array_Ar = []
    for i in data:
        dai = i[5] * math.sqrt(math.pow(i[4] - i[2], 2) + math.pow(i[3] - i[1], 2))
        array_Ar.append(dai)
    array_Ar = np.array(array_Ar)
    # =======
    Ar = np.sum(array_Ar)
    # =======
    # First moment of area X
    array_Sx0 = []
    for i in data:
        sx0i = (i[2] + i[4]) * (i[5] * math.sqrt(math.pow(i[4] - i[2], 2) + math.pow(i[3] - i[1], 2))) / 2
        array_Sx0.append(sx0i)
    array_Sx0 = np.array(array_Sx0)
    Sx0 = np.sum(array_Sx0)
    # =======
    ygc = Sx0 / Ar
    # =======
    # Second moment of area X
    array_Ix0 = []
    for i in data:
        Ix0 = (math.pow(i[2], 2) + math.pow(i[4], 2) + i[2] * i[4]) * (
                i[5] * math.sqrt(math.pow(i[4] - i[2], 2) + math.pow(i[3] - i[1], 2)) / 3)
        array_Ix0.append(Ix0)
    array_Ix0 = np.array(array_Ix0)
    Ix0 = np.sum(array_Ix0)
    # =======
    Ix = Ix0 - Ar * math.pow(ygc, 2)
    # =======

    # First moment of area Y
    array_Sy0 = []
    for i in data:
        sx0i = (i[1] + i[3]) * (i[5] * math.sqrt(math.pow(i[4] - i[2], 2) + math.pow(i[3] - i[1], 2))) / 2
        array_Sy0.append(sx0i)
    array_Sy0 = np.array(array_Sy0)
    Sy0 = np.sum(array_Sy0)
    # =======
    xgc = Sy0 / Ar
    # =======
    # Second moment of area Y
    array_Iy0 = []
    for i in data:
        Iy0 = (math.pow(i[1], 2) + math.pow(i[3], 2) + i[1] * i[3]) * (
                i[5] * math.sqrt(math.pow(i[4] - i[2], 2) + math.pow(i[3] - i[1], 2)) / 3)
        array_Iy0.append(Iy0)
    array_Iy0 = np.array(array_Iy0)
    Iy0 = np.sum(array_Iy0)
    # =======
    Iy = Iy0 - Ar * math.pow(xgc, 2)
    # =======
    return Ar, ygc, Ix, xgc, Iy


class OldMethod:
    def __init__(self):
        # Variables for bending about strong axis
        self.BendStrong_elementData2 = None
        self.BendStrong_ygct = None  # Top flange extreme fiber to neutral axis
        self.BendStrong_ygc = None  # Bottom flange extreme fiber to neutral axis
        self.BendStrong_Ixeff = None  # Moment of inertia
        self.BendStrong_Wxeff = None  # Section modulus
        self.calcs_BendingStrong()
        # Variables for axial compression
        self.Axial_elementData2 = None
        self.Axial_Aeff = None
        self.Axial_ygct = None
        self.Axial_ygc = None
        self.calcs_AxialCompression()

        # Section parts
        #         6       7
        #       ┌────   ────┐    ↑
        #       │           │ 8  │
        #       │ 5              hc
        #                        │
        #       │                ↓
        #     --│-------------------
        #       │
        #       │ 4
        #       │           │ 1
        #       └────   ────┘
        #          3      2

    def calcs_BendingStrong(self):
        # Design Stress
        scomed = defin.steel.fy
        # ==============================================================================================================
        # Effective width of the top flange
        # ==============================================================================================================
        top_flg_stress_ratio = Sec4.stres_ratio(defin.section.bb, 0.0)  # bwhole is 0 for uniform stress.
        top_flg_ksigma = Sec4.Table4_1_ksigma(top_flg_stress_ratio)
        top_flg_lamp = Sec4.lamp(defin.section.bb, defin.section.tcore, top_flg_ksigma, scomed, True)
        top_flg_rho = Sec4.internal_element(top_flg_lamp, top_flg_stress_ratio)
        top_flg_beff = Sec4.Table4_1_beff(top_flg_stress_ratio, defin.section.bb, top_flg_rho)[0]
        top_flg_be1 = Sec4.Table4_1_beff(top_flg_stress_ratio, defin.section.bb, top_flg_rho)[1]
        top_flg_be2 = Sec4.Table4_1_beff(top_flg_stress_ratio, defin.section.bb, top_flg_rho)[2]
        # ==============================================================================================================
        # Effective width of the bot flange
        # ==============================================================================================================
        bot_flg_stress_ratio = Sec4.stres_ratio(defin.section.bb, 0.0)  # bwhole is 0 for uniform stress.
        bot_flg_ksigma = Sec4.Table4_1_ksigma(bot_flg_stress_ratio)
        bot_flg_lamp = Sec4.lamp(defin.section.bb, defin.section.tcore, bot_flg_ksigma, scomed, False)
        bot_flg_rho = Sec4.internal_element(bot_flg_lamp, bot_flg_stress_ratio)
        bot_flg_beff = Sec4.Table4_1_beff(bot_flg_stress_ratio, defin.section.bb, bot_flg_rho)[0]
        bot_flg_be1 = Sec4.Table4_1_beff(bot_flg_stress_ratio, defin.section.bb, bot_flg_rho)[1]
        bot_flg_be2 = Sec4.Table4_1_beff(bot_flg_stress_ratio, defin.section.bb, bot_flg_rho)[2]
        # ==============================================================================================================
        # Effective width of the top edge fold
        # ==============================================================================================================
        top_lip_stres_ratio = Sec4.stres_ratio(defin.section.cc, 0.0)  # bwhole is 0 for uniform stress.
        top_lip_ksigma = Sec553.ksig(defin.section.cc, defin.section.bb)
        top_lip_lamp = Sec4.lamp(defin.section.cc, defin.section.tcore, top_lip_ksigma, scomed, True)
        top_lip_rho = Sec4.outstand_element(top_lip_lamp)
        top_lip_beff = Sec4.Table4_2_beff(defin.section.cc, top_lip_rho, top_lip_stres_ratio)[0]
        top_lip_bc = Sec4.Table4_2_beff(defin.section.cc, top_lip_rho, top_lip_stres_ratio)[1]
        top_lip_bt = Sec4.Table4_2_beff(defin.section.cc, top_lip_rho, top_lip_stres_ratio)[2]
        # Effective area of the edge stiffener
        top_As = defin.section.tcore * (top_flg_be2 + top_lip_beff)
        # Spring stiffness of the edge stiffener
        top_b1 = Sec553.calc_b1(defin.section.bb, top_flg_be2, defin.section.tcore, top_lip_beff)
        top_K = Sec553.springStiffnessK(defin.steel.E, defin.section.tcore, defin.steel.v, top_b1, defin.section.aa,
                                        top_b1, True)
        top_Is = Sec553.Is(top_flg_be2, defin.section.tcore, top_lip_beff)
        top_scrs = Sec553.calc_scrs(top_K, top_Is, defin.steel.E, top_As)
        # Thickness reduction factor
        top_xd = Sec553.thk_reduction(scomed, top_scrs)
        top_t_red = top_xd * defin.section.tcore
        # ==============================================================================================================
        # Effective width of the bottom edge fold
        # ==============================================================================================================
        bot_lip_stres_ratio = Sec4.stres_ratio(defin.section.cc, 0.0)  # bwhole is 0 for uniform stress.
        bot_lip_ksigma = Sec553.ksig(defin.section.cc, defin.section.bb)
        bot_lip_lamp = Sec4.lamp(defin.section.cc, defin.section.tcore, bot_lip_ksigma, scomed, False)
        bot_lip_rho = Sec4.outstand_element(bot_lip_lamp)
        bot_lip_beff = Sec4.Table4_2_beff(defin.section.cc, bot_lip_rho, bot_lip_stres_ratio)[0]
        bot_lip_bc = Sec4.Table4_2_beff(defin.section.cc, bot_lip_rho, bot_lip_stres_ratio)[1]
        bot_lip_bt = Sec4.Table4_2_beff(defin.section.cc, bot_lip_rho, bot_lip_stres_ratio)[2]
        # Effective area of the edge stiffener
        bot_As = defin.section.tcore * (bot_flg_be2 + bot_lip_beff)
        # Spring stiffness of the edge stiffener
        bot_b1 = Sec553.calc_b1(defin.section.bb, bot_flg_be2, defin.section.tcore, bot_lip_beff)
        bot_K = Sec553.springStiffnessK(defin.steel.E, defin.section.tcore, defin.steel.v, bot_b1, defin.section.aa,
                                        bot_b1, True)
        bot_Is = Sec553.Is(bot_flg_be2, defin.section.tcore, bot_lip_beff)
        bot_scrs = Sec553.calc_scrs(bot_K, bot_Is, defin.steel.E, bot_As)
        # Thickness reduction factor
        bot_xd = 1.0  # Tension on bottom flange
        bot_t_red = bot_xd * defin.section.tcore
        print('Iteration is ignored. ScomEd = fy')
        # ==============================================================================================================
        # Effective width of the web
        # ==============================================================================================================
        elementData1 = np.array(
            [[1, defin.section.bb, bot_lip_beff, defin.section.bb, 0.0, bot_t_red],
             [2, defin.section.bb, 0.0, defin.section.bb - bot_flg_be2, 0.0, bot_t_red],
             [3, bot_flg_be1, 0.0, 0.0, 0.0, defin.section.tcore],
             [6, 0.0, defin.section.aa, top_flg_be1, defin.section.aa, defin.section.tcore],
             [7, defin.section.bb - top_flg_be2, defin.section.aa, defin.section.bb, defin.section.aa, top_t_red],
             [8, defin.section.bb, defin.section.aa, defin.section.bb, defin.section.aa - top_lip_beff, top_t_red]])
        # Distance from tension (bottom) flange
        ht = calcEffectiveProps(elementData1)[1]
        # Distance from compression (top) flange
        hc = defin.section.aa - ht
        # Stress ratio
        ff = (hc - defin.section.aa) / hc
        web_ksigma = Sec4.Table4_1_ksigma(ff)
        web_lamp = Sec4.lamp(defin.section.aa, defin.section.tcore, web_ksigma, scomed, True)
        web_rho = Sec4.internal_element(web_lamp, ff)
        web_beff = Sec4.Table4_1_beff(ff, defin.section.aa, web_rho)[0]
        web_be1 = Sec4.Table4_1_beff(ff, defin.section.aa, web_rho)[1]
        web_be2 = Sec4.Table4_1_beff(ff, defin.section.aa, web_rho)[2]
        h1 = web_be1
        h2 = defin.section.aa - (hc - web_be2)
        # ==============================================================================================================
        # Effective section properties
        # ==============================================================================================================
        # Create a matrix contains the element data from bottom lip to top lip
        # 0 id , 1 inodeX, 2 inodeY, 3 jnodeX, 4 JnodeY, 5 thickness
        self.BendStrong_elementData2 = np.array(
            [[1, defin.section.bb, bot_lip_beff, defin.section.bb, 0.0, bot_t_red],
             [2, defin.section.bb, 0.0, defin.section.bb - bot_flg_be2, 0.0, bot_t_red],
             [3, bot_flg_be1, 0.0, 0.0, 0.0, defin.section.tcore],
             [4, 0.0, 0.0, 0.0, h2, defin.section.tcore],
             [5, 0.0, defin.section.aa - h1, 0.0, defin.section.aa, defin.section.tcore],
             [6, 0.0, defin.section.aa, top_flg_be1, defin.section.aa, defin.section.tcore],
             [7, defin.section.bb - top_flg_be2, defin.section.aa, defin.section.bb, defin.section.aa, top_t_red],
             [8, defin.section.bb, defin.section.aa, defin.section.bb, defin.section.aa - top_lip_beff, top_t_red]])

        for i in self.BendStrong_elementData2:
            x = [i[1], i[3]]
            y = [i[2], i[4]]
            t = i[5]
            plt.plot(x, y, linewidth=t)
        plt.axis('equal')
        plt.show()

        # Results
        self.BendStrong_Ixeff = calcEffectiveProps(self.BendStrong_elementData2)[2]
        self.BendStrong_ygc = calcEffectiveProps(self.BendStrong_elementData2)[1]
        self.BendStrong_ygct = defin.section.aa - calcEffectiveProps(self.BendStrong_elementData2)[1]
        self.BendStrong_Wxeff = calcEffectiveProps(self.BendStrong_elementData2)[2] / (
                defin.section.aa - calcEffectiveProps(self.BendStrong_elementData2)[1])

        print('end of bending about strong axis')

    def calcs_AxialCompression(self):
        # Design Stress
        scomed = defin.steel.fy
        # ==============================================================================================================
        # Effective width of the top flange
        # ==============================================================================================================
        top_flg_stress_ratio = Sec4.stres_ratio(defin.section.bb, 0.0)  # bwhole is 0 for uniform stress.
        top_flg_ksigma = Sec4.Table4_1_ksigma(top_flg_stress_ratio)
        top_flg_lamp = Sec4.lamp(defin.section.bb, defin.section.tcore, top_flg_ksigma, scomed, True)
        top_flg_rho = Sec4.internal_element(top_flg_lamp, top_flg_stress_ratio)
        top_flg_beff = Sec4.Table4_1_beff(top_flg_stress_ratio, defin.section.bb, top_flg_rho)[0]
        top_flg_be1 = Sec4.Table4_1_beff(top_flg_stress_ratio, defin.section.bb, top_flg_rho)[1]
        top_flg_be2 = Sec4.Table4_1_beff(top_flg_stress_ratio, defin.section.bb, top_flg_rho)[2]
        # ==============================================================================================================
        # Effective width of the bot flange
        # ==============================================================================================================
        bot_flg_stress_ratio = Sec4.stres_ratio(defin.section.bb, 0.0)  # bwhole is 0 for uniform stress.
        bot_flg_ksigma = Sec4.Table4_1_ksigma(bot_flg_stress_ratio)
        bot_flg_lamp = Sec4.lamp(defin.section.bb, defin.section.tcore, bot_flg_ksigma, scomed, True)
        bot_flg_rho = Sec4.internal_element(bot_flg_lamp, bot_flg_stress_ratio)
        bot_flg_beff = Sec4.Table4_1_beff(bot_flg_stress_ratio, defin.section.bb, bot_flg_rho)[0]
        bot_flg_be1 = Sec4.Table4_1_beff(bot_flg_stress_ratio, defin.section.bb, bot_flg_rho)[1]
        bot_flg_be2 = Sec4.Table4_1_beff(bot_flg_stress_ratio, defin.section.bb, bot_flg_rho)[2]
        # ==============================================================================================================
        # Effective width of the top edge fold
        # ==============================================================================================================
        top_lip_stres_ratio = Sec4.stres_ratio(defin.section.cc, 0.0)  # bwhole is 0 for uniform stress.
        top_lip_ksigma = Sec553.ksig(defin.section.cc, defin.section.bb)
        top_lip_lamp = Sec4.lamp(defin.section.cc, defin.section.tcore, top_lip_ksigma, scomed, True)
        top_lip_rho = Sec4.outstand_element(top_lip_lamp)
        top_lip_beff = Sec4.Table4_2_beff(defin.section.cc, top_lip_rho, top_lip_stres_ratio)[0]
        top_lip_bc = Sec4.Table4_2_beff(defin.section.cc, top_lip_rho, top_lip_stres_ratio)[1]
        top_lip_bt = Sec4.Table4_2_beff(defin.section.cc, top_lip_rho, top_lip_stres_ratio)[2]
        # Effective area of the edge stiffener
        top_As = defin.section.tcore * (top_flg_be2 + top_lip_beff)
        # Spring stiffness of the edge stiffener
        top_b1 = Sec553.calc_b1(defin.section.bb, top_flg_be2, defin.section.tcore, top_lip_beff)
        top_K = Sec553.springStiffnessK(defin.steel.E, defin.section.tcore, defin.steel.v, top_b1, defin.section.aa,
                                        top_b1, False)
        top_Is = Sec553.Is(top_flg_be2, defin.section.tcore, top_lip_beff)
        top_scrs = Sec553.calc_scrs(top_K, top_Is, defin.steel.E, top_As)
        # Thickness reduction factor
        top_xd = Sec553.thk_reduction(scomed, top_scrs)
        top_t_red = top_xd * defin.section.tcore
        # ==============================================================================================================
        # Effective width of the bottom edge fold
        # ==============================================================================================================
        bot_lip_stres_ratio = Sec4.stres_ratio(defin.section.cc, 0.0)  # bwhole is 0 for uniform stress.
        bot_lip_ksigma = Sec553.ksig(defin.section.cc, defin.section.bb)
        bot_lip_lamp = Sec4.lamp(defin.section.cc, defin.section.tcore, bot_lip_ksigma, scomed, True)
        bot_lip_rho = Sec4.outstand_element(bot_lip_lamp)
        bot_lip_beff = Sec4.Table4_2_beff(defin.section.cc, bot_lip_rho, bot_lip_stres_ratio)[0]
        bot_lip_bc = Sec4.Table4_2_beff(defin.section.cc, bot_lip_rho, bot_lip_stres_ratio)[1]
        bot_lip_bt = Sec4.Table4_2_beff(defin.section.cc, bot_lip_rho, bot_lip_stres_ratio)[2]
        # Effective area of the edge stiffener
        bot_As = defin.section.tcore * (bot_flg_be2 + bot_lip_beff)
        # Spring stiffness of the edge stiffener
        bot_b1 = Sec553.calc_b1(defin.section.bb, bot_flg_be2, defin.section.tcore, bot_lip_beff)
        bot_K = Sec553.springStiffnessK(defin.steel.E, defin.section.tcore, defin.steel.v, bot_b1, defin.section.aa,
                                        bot_b1, False)
        bot_Is = Sec553.Is(bot_flg_be2, defin.section.tcore, bot_lip_beff)
        bot_scrs = Sec553.calc_scrs(bot_K, bot_Is, defin.steel.E, bot_As)
        # Thickness reduction factor
        bot_xd = Sec553.thk_reduction(scomed, bot_scrs)
        bot_t_red = bot_xd * defin.section.tcore
        print('Iteration is ignored. ScomEd = fy')
        # ==============================================================================================================
        # Effective width of the web
        # ==============================================================================================================
        elementData1 = np.array(
            [[1, defin.section.bb, bot_lip_beff, defin.section.bb, 0.0, bot_t_red],
             [2, defin.section.bb, 0.0, defin.section.bb - bot_flg_be2, 0.0, bot_t_red],
             [3, bot_flg_be1, 0.0, 0.0, 0.0, defin.section.tcore],
             [6, 0.0, defin.section.aa, top_flg_be1, defin.section.aa, defin.section.tcore],
             [7, defin.section.bb - top_flg_be2, defin.section.aa, defin.section.bb, defin.section.aa, top_t_red],
             [8, defin.section.bb, defin.section.aa, defin.section.bb, defin.section.aa - top_lip_beff, top_t_red]])
        # Distance from tension (bottom) flange
        ht = calcEffectiveProps(elementData1)[1]
        # Distance from compression (top) flange
        hc = defin.section.aa - ht
        # Stress ratio
        ff = 1.0  # uniform compression
        web_ksigma = Sec4.Table4_1_ksigma(ff)
        web_lamp = Sec4.lamp(defin.section.aa, defin.section.tcore, web_ksigma, scomed, True)
        web_rho = Sec4.internal_element(web_lamp, ff)
        web_beff = Sec4.Table4_1_beff(ff, defin.section.aa, web_rho)[0]
        web_be1 = Sec4.Table4_1_beff(ff, defin.section.aa, web_rho)[1]
        web_be2 = Sec4.Table4_1_beff(ff, defin.section.aa, web_rho)[2]
        h1 = web_be1
        h2 = web_be2
        # ==============================================================================================================
        # Effective section properties
        # ==============================================================================================================
        # Create a matrix contains the element data from bottom lip to top lip
        # 0 id , 1 inodeX, 2 inodeY, 3 jnodeX, 4 JnodeY, 5 thickness
        self.Axial_elementData2 = np.array(
            [[1, defin.section.bb, bot_lip_beff, defin.section.bb, 0.0, bot_t_red],
             [2, defin.section.bb, 0.0, defin.section.bb - bot_flg_be2, 0.0, bot_t_red],
             [3, bot_flg_be1, 0.0, 0.0, 0.0, defin.section.tcore],
             [4, 0.0, 0.0, 0.0, h2, defin.section.tcore],
             [5, 0.0, defin.section.aa - h1, 0.0, defin.section.aa, defin.section.tcore],
             [6, 0.0, defin.section.aa, top_flg_be1, defin.section.aa, defin.section.tcore],
             [7, defin.section.bb - top_flg_be2, defin.section.aa, defin.section.bb, defin.section.aa, top_t_red],
             [8, defin.section.bb, defin.section.aa, defin.section.bb, defin.section.aa - top_lip_beff, top_t_red]])

        for i in self.Axial_elementData2:
            x = [i[1], i[3]]
            y = [i[2], i[4]]
            t = i[5]
            plt.plot(x, y, linewidth=t)
        plt.axis('equal')
        plt.show()

        # Results
        self.Axial_ygc = calcEffectiveProps(self.Axial_elementData2)[1]
        self.Axial_ygct = defin.section.aa - calcEffectiveProps(self.Axial_elementData2)[1]
        self.Axial_Aeff = calcEffectiveProps(self.Axial_elementData2)[0]

        print('end of axial compression')

    def calcs_BendingWeakWeb(self):
        """
        This function calculates the effective section properties for bending about weak axis and web is under
        compression.
        """
        # Design Stress
        scomed = defin.steel.fy
        # ==============================================================================================================
        # Effective width of the web
        # ==============================================================================================================
        web_stress_ratio = Sec4.stres_ratio(defin.section.aa, 0.0)  # bwhole is 0 for uniform stress.
        web_ksigma = Sec4.Table4_1_ksigma(web_stress_ratio)
        web_lamp = Sec4.lamp(defin.section.aa, defin.section.tcore, web_ksigma, scomed, True)
        web_rho = Sec4.internal_element(web_lamp, web_stress_ratio)
        web_beff = Sec4.Table4_1_beff(web_stress_ratio, defin.section.aa, web_rho)[0]
        web_be1 = Sec4.Table4_1_beff(web_stress_ratio, defin.section.aa, web_rho)[1]
        web_be2 = Sec4.Table4_1_beff(web_stress_ratio, defin.section.aa, web_rho)[2]
        # ==================================================
        # Locate the neutral axis
        elementData1 = np.array(
            [[1, defin.section.bb, defin.section.cc, defin.section.bb, 0.0, defin.section.tcore],
             [2, defin.section.bb, 0.0, defin.section.bb/2, 0.0, defin.section.tcore],
             [3, defin.section.bb/2, 0.0, 0.0, 0.0, defin.section.tcore],
             [6, 0.0, defin.section.aa, top_flg_be1, defin.section.aa, defin.section.tcore],
             [7, defin.section.bb - top_flg_be2, defin.section.aa, defin.section.bb, defin.section.aa, top_t_red],
             [8, defin.section.bb, defin.section.aa, defin.section.bb, defin.section.aa - top_lip_beff, top_t_red]])
        # Distance from tension (bottom) flange
        ht = calcEffectiveProps(elementData1)[1]
        # Distance from compression (top) flange
        hc = defin.section.aa - ht


        # ==============================================================================================================
        # Effective width of the bot flange
        # ==============================================================================================================
        bot_flg_stress_ratio = Sec4.stres_ratio(defin.section.bb, 0.0)  # bwhole is 0 for uniform stress.
        bot_flg_ksigma = Sec4.Table4_1_ksigma(bot_flg_stress_ratio)
        bot_flg_lamp = Sec4.lamp(defin.section.bb, defin.section.tcore, bot_flg_ksigma, scomed, False)
        bot_flg_rho = Sec4.internal_element(bot_flg_lamp, bot_flg_stress_ratio)
        bot_flg_beff = Sec4.Table4_1_beff(bot_flg_stress_ratio, defin.section.bb, bot_flg_rho)[0]
        bot_flg_be1 = Sec4.Table4_1_beff(bot_flg_stress_ratio, defin.section.bb, bot_flg_rho)[1]
        bot_flg_be2 = Sec4.Table4_1_beff(bot_flg_stress_ratio, defin.section.bb, bot_flg_rho)[2]
        # ==============================================================================================================
        # Effective width of the top edge fold
        # ==============================================================================================================
        top_lip_stres_ratio = Sec4.stres_ratio(defin.section.cc, 0.0)  # bwhole is 0 for uniform stress.
        top_lip_ksigma = Sec553.ksig(defin.section.cc, defin.section.bb)
        top_lip_lamp = Sec4.lamp(defin.section.cc, defin.section.tcore, top_lip_ksigma, scomed, True)
        top_lip_rho = Sec4.outstand_element(top_lip_lamp)
        top_lip_beff = Sec4.Table4_2_beff(defin.section.cc, top_lip_rho, top_lip_stres_ratio)[0]
        top_lip_bc = Sec4.Table4_2_beff(defin.section.cc, top_lip_rho, top_lip_stres_ratio)[1]
        top_lip_bt = Sec4.Table4_2_beff(defin.section.cc, top_lip_rho, top_lip_stres_ratio)[2]
        # Effective area of the edge stiffener
        top_As = defin.section.tcore * (top_flg_be2 + top_lip_beff)
        # Spring stiffness of the edge stiffener
        top_b1 = Sec553.calc_b1(defin.section.bb, top_flg_be2, defin.section.tcore, top_lip_beff)
        top_K = Sec553.springStiffnessK(defin.steel.E, defin.section.tcore, defin.steel.v, top_b1, defin.section.aa,
                                        top_b1, True)
        top_Is = Sec553.Is(top_flg_be2, defin.section.tcore, top_lip_beff)
        top_scrs = Sec553.calc_scrs(top_K, top_Is, defin.steel.E, top_As)
        # Thickness reduction factor
        top_xd = Sec553.thk_reduction(scomed, top_scrs)
        top_t_red = top_xd * defin.section.tcore
        # ==============================================================================================================
        # Effective width of the bottom edge fold
        # ==============================================================================================================
        bot_lip_stres_ratio = Sec4.stres_ratio(defin.section.cc, 0.0)  # bwhole is 0 for uniform stress.
        bot_lip_ksigma = Sec553.ksig(defin.section.cc, defin.section.bb)
        bot_lip_lamp = Sec4.lamp(defin.section.cc, defin.section.tcore, bot_lip_ksigma, scomed, False)
        bot_lip_rho = Sec4.outstand_element(bot_lip_lamp)
        bot_lip_beff = Sec4.Table4_2_beff(defin.section.cc, bot_lip_rho, bot_lip_stres_ratio)[0]
        bot_lip_bc = Sec4.Table4_2_beff(defin.section.cc, bot_lip_rho, bot_lip_stres_ratio)[1]
        bot_lip_bt = Sec4.Table4_2_beff(defin.section.cc, bot_lip_rho, bot_lip_stres_ratio)[2]
        # Effective area of the edge stiffener
        bot_As = defin.section.tcore * (bot_flg_be2 + bot_lip_beff)
        # Spring stiffness of the edge stiffener
        bot_b1 = Sec553.calc_b1(defin.section.bb, bot_flg_be2, defin.section.tcore, bot_lip_beff)
        bot_K = Sec553.springStiffnessK(defin.steel.E, defin.section.tcore, defin.steel.v, bot_b1, defin.section.aa,
                                        bot_b1, True)
        bot_Is = Sec553.Is(bot_flg_be2, defin.section.tcore, bot_lip_beff)
        bot_scrs = Sec553.calc_scrs(bot_K, bot_Is, defin.steel.E, bot_As)
        # Thickness reduction factor
        bot_xd = 1.0  # Tension on bottom flange
        bot_t_red = bot_xd * defin.section.tcore
        print('Iteration is ignored. ScomEd = fy')
        # ==============================================================================================================
        # Effective width of the web
        # ==============================================================================================================
        elementData1 = np.array(
            [[1, defin.section.bb, bot_lip_beff, defin.section.bb, 0.0, bot_t_red],
             [2, defin.section.bb, 0.0, defin.section.bb - bot_flg_be2, 0.0, bot_t_red],
             [3, bot_flg_be1, 0.0, 0.0, 0.0, defin.section.tcore],
             [6, 0.0, defin.section.aa, top_flg_be1, defin.section.aa, defin.section.tcore],
             [7, defin.section.bb - top_flg_be2, defin.section.aa, defin.section.bb, defin.section.aa, top_t_red],
             [8, defin.section.bb, defin.section.aa, defin.section.bb, defin.section.aa - top_lip_beff, top_t_red]])
        # Distance from tension (bottom) flange
        ht = calcEffectiveProps(elementData1)[1]
        # Distance from compression (top) flange
        hc = defin.section.aa - ht
        # Stress ratio
        ff = (hc - defin.section.aa) / hc
        web_ksigma = Sec4.Table4_1_ksigma(ff)
        web_lamp = Sec4.lamp(defin.section.aa, defin.section.tcore, web_ksigma, scomed, True)
        web_rho = Sec4.internal_element(web_lamp, ff)
        web_beff = Sec4.Table4_1_beff(ff, defin.section.aa, web_rho)[0]
        web_be1 = Sec4.Table4_1_beff(ff, defin.section.aa, web_rho)[1]
        web_be2 = Sec4.Table4_1_beff(ff, defin.section.aa, web_rho)[2]
        h1 = web_be1
        h2 = defin.section.aa - (hc - web_be2)
        # ==============================================================================================================
        # Effective section properties
        # ==============================================================================================================
        # Create a matrix contains the element data from bottom lip to top lip
        # 0 id , 1 inodeX, 2 inodeY, 3 jnodeX, 4 JnodeY, 5 thickness
        self.BendStrong_elementData2 = np.array(
            [[1, defin.section.bb, bot_lip_beff, defin.section.bb, 0.0, bot_t_red],
             [2, defin.section.bb, 0.0, defin.section.bb - bot_flg_be2, 0.0, bot_t_red],
             [3, bot_flg_be1, 0.0, 0.0, 0.0, defin.section.tcore],
             [4, 0.0, 0.0, 0.0, h2, defin.section.tcore],
             [5, 0.0, defin.section.aa - h1, 0.0, defin.section.aa, defin.section.tcore],
             [6, 0.0, defin.section.aa, top_flg_be1, defin.section.aa, defin.section.tcore],
             [7, defin.section.bb - top_flg_be2, defin.section.aa, defin.section.bb, defin.section.aa, top_t_red],
             [8, defin.section.bb, defin.section.aa, defin.section.bb, defin.section.aa - top_lip_beff, top_t_red]])

        for i in self.BendStrong_elementData2:
            x = [i[1], i[3]]
            y = [i[2], i[4]]
            t = i[5]
            plt.plot(x, y, linewidth=t)
        plt.axis('equal')
        plt.show()

        # Results
        self.BendStrong_Ixeff = calcEffectiveProps(self.BendStrong_elementData2)[2]
        self.BendStrong_ygc = calcEffectiveProps(self.BendStrong_elementData2)[1]
        self.BendStrong_ygct = defin.section.aa - calcEffectiveProps(self.BendStrong_elementData2)[1]
        self.BendStrong_Wxeff = calcEffectiveProps(self.BendStrong_elementData2)[2] / (
                defin.section.aa - calcEffectiveProps(self.BendStrong_elementData2)[1])

        print('end of bending about strong axis')




sec = OldMethod()
print(sec.Axial_Aeff)
