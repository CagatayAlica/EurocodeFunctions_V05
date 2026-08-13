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

    def __str__(self):
        rep = 'MATERIAL PROPERTIES \n'
        rep += (f"Name {self.name} \n"
                f"fy \t= {self.fy:.1f} MPa\n"
                f"fu \t= {self.fu:.1f} MPa,\n"
                f"E \t= {self.E:.1f} MPa,\n"
                f"v \t= {self.v:.1f},\n"
                f"G \t= {self.G:.1f} MPa,\n"
                f"eps\t= {self.eps:.3f}, \n")
        return rep