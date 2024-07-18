class userInputs:
    def __init__(self):
        self.C1 = None
        self.Lt = None
        self.Ly = None
        self.Lx = None
        self.fu = None
        self.fy = None
        self.MatName = None
        self.R = None
        self.t = None
        self.C = None
        self.B = None
        self.A = None
        self.P = None
        self.Mx = None
        self.My = None
        self.Vy = None
        self.Vx = None
        self.main()

    def main(self):
        # Main inputs for the calculations:
        # ==== Sections ====
        self.A: float = 200.0
        self.B: float = 55.0
        self.C: float = 10.0
        self.t: float = 1.6
        self.R: float = 1.6
        # ==== Material ====
        self.MatName: str = 'S280'
        self.fy: float = 350.0
        self.fu: float = 380.0
        # ==== Member ====
        self.Lx: float = 2800.0
        self.Ly: float = 1220.0
        self.Lt: float = 1220.0
        self.C1: float = 1.127
        # ==== Loads ====
        self.P: float = -23.0  # + for tension, - for compression
        self.Mx: float = 35.0  # + for compression on top flange
        self.My: float = 0.20  # + for compression on web
        self.Vy: float = 12.0  # Shear along web
        self.Vx: float = 0.00  # Shear along flanges
