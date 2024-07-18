import numpy as np
import math


class GrossProperties:
    def __init__(self, x: list[float], y: list[float], t: float, r: float):
        self.xo = None
        self.It = None
        self.Cw = None
        self.ysc = None
        self.xsc = None
        self.Iw = None
        self.Ixy = None
        self.Wy = None
        self.Iy = None
        self.Wx = None
        self.Ix = None
        self.zgy = None
        self.zgx = None
        self.Ar = None
        self.x = x
        self.y = y
        self.t = t
        self.r = r
        self.prop = None
        self.grossProp(self.x, self.y, self.t, self.r)

    def grossProp(self, x, y, t, r):
        # Area of cross-section
        da = np.zeros([len(x)])
        ba = np.zeros([len(x)])
        for i in range(1, len(da)):
            da[i] = math.sqrt(math.pow(x[i - 1] - x[i], 2) + math.pow(y[i - 1] - y[i], 2)) * t
            ba[i] = math.sqrt(math.pow(x[i - 1] - x[i], 2) + math.pow(y[i - 1] - y[i], 2))
        Ar = np.sum(da)
        Lt = np.sum(ba)
        # Total rj.tetaj/90
        Trj = 4 * 4 * r * (1.0 / 4.0)
        delta = 0.43 * Trj / Lt
        # First moment of area and coordinate for gravity centre
        sx0 = np.zeros([len(x)])
        sy0 = np.zeros([len(x)])
        for i in range(1, len(sx0)):
            sx0[i] = (y[i] + y[i - 1]) * da[i] / 2
        zgy = np.sum(sx0) / Ar
        for i in range(1, len(sy0)):
            sy0[i] = (x[i] + x[i - 1]) * da[i] / 2
        zgx = np.sum(sy0) / Ar

        # Second moment of area
        Ix0 = np.zeros([len(x)])
        Iy0 = np.zeros([len(x)])
        for i in range(1, len(Ix0)):
            Ix0[i] = (math.pow(y[i], 2) + math.pow(y[i - 1], 2) + y[i] * y[i - 1]) * da[i] / 3
        for i in range(1, len(Iy0)):
            Iy0[i] = (math.pow(x[i], 2) + math.pow(x[i - 1], 2) + x[i] * x[i - 1]) * da[i] / 3
        Ix = np.sum(Ix0) - Ar * math.pow(zgy, 2)
        Iy = np.sum(Iy0) - Ar * math.pow(zgx, 2)

        # Product moment of area
        Ixy0 = np.zeros([len(x)])
        for i in range(1, len(Ixy0)):
            Ixy0[i] = (2 * x[i - 1] * y[i - 1] + 2 * x[i] * y[i] + x[i - 1] * y[i] + x[i] * y[i - 1]) * da[i] / 6
        Ixy = np.sum(Ixy0) - (np.sum(sx0) * np.sum(sy0)) / Ar

        # Principle axis
        alfa = 0.5 * math.atan(2 * Ixy / (Iy - Ix))
        Iksi = 0.5 * (Ix + Iy + math.sqrt(math.pow(Iy - Ix, 2) + 4 * math.pow(Ixy, 2)))
        Ieta = 0.5 * (Ix + Iy - math.sqrt(math.pow(Iy - Ix, 2) + 4 * math.pow(Ixy, 2)))

        # Sectoral coordinates
        w = np.zeros([len(x)])
        w0 = np.zeros([len(x)])
        Iw = np.zeros([len(x)])
        w0[0] = 0
        for i in range(1, len(w0)):
            w0[i] = x[i - 1] * y[i] - x[i] * y[i - 1]
            w[i] = w[i - 1] + w0[i]
            Iw[i] = (w[i - 1] + w[i]) * da[i] / 2
        wmean = np.sum(Iw) / Ar

        # Sectorial constants
        Ixw0 = np.zeros([len(x)])
        Iyw0 = np.zeros([len(x)])
        Iww0 = np.zeros([len(x)])
        for i in range(1, len(Ixw0)):
            Ixw0[i] = (2 * x[i - 1] * w[i - 1] + 2 * x[i] * w[i] + x[i - 1] * w[i] + x[i] * w[i - 1]) * da[i] / 6
            Iyw0[i] = (2 * y[i - 1] * w[i - 1] + 2 * y[i] * w[i] + y[i - 1] * w[i] + y[i] * w[i - 1]) * da[i] / 6
            Iww0[i] = (math.pow(w[i], 2) + math.pow(w[i - 1], 2) + w[i] * w[i - 1]) * da[i] / 3
        Ixw = np.sum(Ixw0) - np.sum(sy0) * np.sum(Iw) / Ar
        Iyw = np.sum(Iyw0) - np.sum(sx0) * np.sum(Iw) / Ar
        Iww = np.sum(Iww0) - math.pow(np.sum(Iw), 2) / Ar

        # Shear centre
        xsc = (Iyw * Iy - Ixw * Ixy) / (Ix * Iy - math.pow(Ixy, 2))
        ysc = (-Ixw * Ix + Iyw * Ixy) / (Ix * Iy - math.pow(Ixy, 2))

        # Warping constant
        Cw = Iww + ysc * Ixw - xsc * Iyw

        # Torsion constant
        It0 = np.zeros([len(x)])
        for i in range(1, len(It0)):
            It0[i] = da[i] * math.pow(t, 2) / 3
        It = np.sum(It0)

        # Distance between centroid and shear centre
        xo = abs(xsc) + zgx
        # Distances from the boundaries
        zgb = zgy
        zgt = max(y) - zgb
        zgl = zgx
        zgr = max(x) - zgl
        # Calculated data
        propData = np.zeros([14])
        propData[0] = Ar * (1 - delta)
        propData[1] = max(zgb, zgt)
        propData[2] = max(zgl, zgr)
        propData[3] = Ix * (1 - 2 * delta)
        propData[4] = Ix * (1 - 2 * delta) / max(zgb, zgt)
        propData[5] = Iy * (1 - 2 * delta)
        propData[6] = Iy * (1 - 2 * delta) / max(zgl, zgr)
        propData[7] = Ixy
        propData[8] = np.sum(Iw)
        propData[9] = xsc
        propData[10] = ysc
        propData[11] = Cw * (1 - 4 * delta)
        propData[12] = It * (1 - 2 * delta)
        propData[13] = xo
        Wx = Ix * (1 - 2 * delta) / max(zgb, zgt)
        Wy = Iy * (1 - 2 * delta) / max(zgl, zgr)
        # Define the attributes
        self.Ar = Ar
        self.zgx = zgx
        self.zgy = zgy
        self.Ix = Ix
        self.Wx = Wx
        self.Iy = Iy
        self.Wy = Wy
        self.Ixy = Ixy
        self.Iw = Iw
        self.xsc = xsc
        self.ysc = ysc
        self.Cw = Cw
        self.It = It
        self.xo = xo

        # Data dictionary
        self.prop = {
            "Ar": Ar,
            "zgx": zgx,
            "zgy": zgy,
            "Ix": Ix,
            "Wx": Ix * (1 - 2 * delta) / max(zgb, zgt),
            "Iy": Iy,
            "Wy": Iy * (1 - 2 * delta) / max(zgl, zgr),
            "Ixy": Ixy,
            "Iw": np.sum(Iw),
            "xsc": xsc,
            "ysc": ysc,
            "Cw": Cw,
            "It": It,
            "xo": xo
        }

        return self.prop, propData
