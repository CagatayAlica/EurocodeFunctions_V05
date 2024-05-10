import math


class material:
    def __init__(self, name, fy, fu):
        self.name = name
        self.fy = fy
        self.fu = fu
        self.E = 210000
        self.v = 0.3
        self.G = self.E / (2 * (1 + self.v))
        self.eps = math.sqrt(235.0/self.fy)

