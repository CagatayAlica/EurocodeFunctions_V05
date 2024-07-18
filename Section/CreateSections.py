import math
import matplotlib.pyplot as plt
import numpy as np


class LippedCSection:
    def __init__(self, A: float, B: float, C: float, t: float, R: float):
        self.thk = t
        self.A = A
        self.B = B
        self.C = C
        self.R = R
        r = R + t / 2.0
        # Centerline dimensions
        aa = A - t
        bb = B - t
        cc = C - t / 2.0
        tcore = t - 0.04
        # Flat portions
        a = aa - 2 * r
        b = bb - 2 * r
        c = cc - r

        self.a = a
        self.b = b
        self.c = c
        self.r = r
        self.aa = aa
        self.bb = bb
        self.cc = cc
        self.tcore = tcore

        def tranform(alfa, origin):
            # Transformation matrix
            p = origin
            c, s = np.cos(math.radians(alfa)), np.sin(math.radians(alfa))
            j = np.array([[c, s, 0],
                          [-s, c, 0],
                          [0, 0, 1]])
            RotatedCorners = np.matmul(j, p)
            return RotatedCorners.T

        # Bottom right
        origin1 = np.array([bb - r, r, 0.0])
        radius = np.array([0, r, 0.0])
        start_ang = 90
        p11 = tranform(start_ang + 10, radius)
        p12 = tranform(start_ang + 20, radius)
        p13 = tranform(start_ang + 30, radius)
        p14 = tranform(start_ang + 40, radius)
        p15 = tranform(start_ang + 50, radius)
        p16 = tranform(start_ang + 60, radius)
        p17 = tranform(start_ang + 70, radius)
        p18 = tranform(start_ang + 80, radius)
        # Bottom left
        origin2 = np.array([r, r, 0.0])
        start_ang = 180
        p21 = tranform(start_ang + 10, radius)
        p22 = tranform(start_ang + 20, radius)
        p23 = tranform(start_ang + 30, radius)
        p24 = tranform(start_ang + 40, radius)
        p25 = tranform(start_ang + 50, radius)
        p26 = tranform(start_ang + 60, radius)
        p27 = tranform(start_ang + 70, radius)
        p28 = tranform(start_ang + 80, radius)
        # Top left
        origin3 = np.array([r, aa - r, 0.0])
        start_ang = 270
        p31 = tranform(start_ang + 10, radius)
        p32 = tranform(start_ang + 20, radius)
        p33 = tranform(start_ang + 30, radius)
        p34 = tranform(start_ang + 40, radius)
        p35 = tranform(start_ang + 50, radius)
        p36 = tranform(start_ang + 60, radius)
        p37 = tranform(start_ang + 70, radius)
        p38 = tranform(start_ang + 80, radius)
        # Top right
        origin4 = np.array([bb - r, aa - r, 0.0])
        start_ang = 0
        p41 = tranform(start_ang + 10, radius)
        p42 = tranform(start_ang + 20, radius)
        p43 = tranform(start_ang + 30, radius)
        p44 = tranform(start_ang + 40, radius)
        p45 = tranform(start_ang + 50, radius)
        p46 = tranform(start_ang + 60, radius)
        p47 = tranform(start_ang + 70, radius)
        p48 = tranform(start_ang + 80, radius)

        self.nodes = np.array([[0, bb, cc, 1, 1, 1, 1, 0],
                               [1, bb, r, 1, 1, 1, 1, 0],
                               [2, origin1[0] + p11[0], origin1[1] + p11[1], 1, 1, 1, 1, 0],
                               [3, origin1[0] + p12[0], origin1[1] + p12[1], 1, 1, 1, 1, 0],
                               [4, origin1[0] + p13[0], origin1[1] + p13[1], 1, 1, 1, 1, 0],
                               [5, origin1[0] + p14[0], origin1[1] + p14[1], 1, 1, 1, 1, 0],
                               [6, origin1[0] + p15[0], origin1[1] + p15[1], 1, 1, 1, 1, 0],
                               [7, origin1[0] + p16[0], origin1[1] + p16[1], 1, 1, 1, 1, 0],
                               [8, origin1[0] + p17[0], origin1[1] + p17[1], 1, 1, 1, 1, 0],
                               [9, origin1[0] + p18[0], origin1[1] + p18[1], 1, 1, 1, 1, 0],
                               [10, bb - r, 0, 1, 1, 1, 1, 0],
                               [11, r + b / 2.0, 0, 1, 1, 1, 1, 0],
                               [12, r, 0, 1, 1, 1, 1, 0],
                               [13, origin2[0] + p21[0], origin2[1] + p21[1], 1, 1, 1, 1, 0],
                               [14, origin2[0] + p22[0], origin2[1] + p22[1], 1, 1, 1, 1, 0],
                               [15, origin2[0] + p23[0], origin2[1] + p23[1], 1, 1, 1, 1, 0],
                               [16, origin2[0] + p24[0], origin2[1] + p24[1], 1, 1, 1, 1, 0],
                               [17, origin2[0] + p25[0], origin2[1] + p25[1], 1, 1, 1, 1, 0],
                               [18, origin2[0] + p26[0], origin2[1] + p26[1], 1, 1, 1, 1, 0],
                               [19, origin2[0] + p27[0], origin2[1] + p27[1], 1, 1, 1, 1, 0],
                               [20, origin2[0] + p28[0], origin2[1] + p28[1], 1, 1, 1, 1, 0],
                               [21, 0, r, 1, 1, 1, 1, 0],
                               [22, 0, r + a * (1.0 / 4.0), 1, 1, 1, 1, 0],
                               [23, 0, r + a * (2.0 / 4.0), 1, 1, 1, 1, 0],
                               [24, 0, r + a * (3.0 / 4.0), 1, 1, 1, 1, 0],
                               [25, 0, r + a, 1, 1, 1, 1, 0],
                               [26, origin3[0] + p31[0], origin3[1] + p31[1], 1, 1, 1, 1, 0],
                               [27, origin3[0] + p32[0], origin3[1] + p32[1], 1, 1, 1, 1, 0],
                               [28, origin3[0] + p33[0], origin3[1] + p33[1], 1, 1, 1, 1, 0],
                               [29, origin3[0] + p34[0], origin3[1] + p34[1], 1, 1, 1, 1, 0],
                               [30, origin3[0] + p35[0], origin3[1] + p35[1], 1, 1, 1, 1, 0],
                               [31, origin3[0] + p36[0], origin3[1] + p36[1], 1, 1, 1, 1, 0],
                               [32, origin3[0] + p37[0], origin3[1] + p37[1], 1, 1, 1, 1, 0],
                               [33, origin3[0] + p38[0], origin3[1] + p38[1], 1, 1, 1, 1, 0],
                               [34, r, aa, 1, 1, 1, 1, 0],
                               [35, r + b / 2.0, aa, 1, 1, 1, 1, 0],
                               [36, bb - r, aa, 1, 1, 1, 1, 0],
                               [37, origin4[0] + p41[0], origin4[1] + p41[1], 1, 1, 1, 1, 0],
                               [38, origin4[0] + p42[0], origin4[1] + p42[1], 1, 1, 1, 1, 0],
                               [39, origin4[0] + p43[0], origin4[1] + p43[1], 1, 1, 1, 1, 0],
                               [40, origin4[0] + p44[0], origin4[1] + p44[1], 1, 1, 1, 1, 0],
                               [41, origin4[0] + p45[0], origin4[1] + p45[1], 1, 1, 1, 1, 0],
                               [42, origin4[0] + p46[0], origin4[1] + p46[1], 1, 1, 1, 1, 0],
                               [43, origin4[0] + p47[0], origin4[1] + p47[1], 1, 1, 1, 1, 0],
                               [44, origin4[0] + p48[0], origin4[1] + p48[1], 1, 1, 1, 1, 0],
                               [45, bb, aa - r, 1, 1, 1, 1, 0],
                               [46, bb, aa - cc, 1, 1, 1, 1, 0]])

        self.elements = np.array([[0, 0, 1, self.thk, 0],
                                  [1, 1, 2, self.thk, 0],
                                  [2, 2, 3, self.thk, 0],
                                  [3, 3, 4, self.thk, 0],
                                  [4, 4, 5, self.thk, 0],
                                  [5, 5, 6, self.thk, 0],
                                  [6, 6, 7, self.thk, 0],
                                  [7, 7, 8, self.thk, 0],
                                  [8, 8, 9, self.thk, 0],
                                  [9, 9, 10, self.thk, 0]
                                  ])
        self.x = self.nodes[:, 1]
        self.y = self.nodes[:, 2]
        self.descp = f'Section : A: {A:.2f}, B: {B:.2f}, C: {C:.2f}, t: {t:.2f}'
        self.x_inches = self.x * 25.4
        self.y_inches = self.y * 25.4
        # Data for plotting
        # plot_C_section(self.x, self.y, self.descp)


def plot_C_section(x, y, title):
    t = x
    s = y
    fig, ax = plt.subplots()
    ax.scatter(t, s)
    ax.set(xlabel='mm', ylabel='mm', title=title)
    ax.grid()
    plt.axis('equal')
    plt.show()
