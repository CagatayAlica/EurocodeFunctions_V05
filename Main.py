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
        self.Ned = None
        self.Medx = None
        self.Medy = None
        self.Vedy = None
        self.Vedx = None
        self.main()

    def main(self):
        # Main inputs for the calculations:
        # ==== Sections ====
        self.A: float = 200.0
        self.B: float = 55.0
        self.C: float = 10.0
        self.t: float = 1.6
        self.R: float = 3.0
        # ==== Material ====
        self.MatName: str = 'S280'
        self.fy: float = 280.0
        self.fu: float = 380.0
        # ==== Member ====
        self.Lx: float = 2800.0
        self.Ly: float = 1220.0
        self.Lt: float = 1220.0
        self.C1: float = 1.127
        # ==== Loads ====
        self.Ned: float = -23.0  # + for tension, - for compression
        self.Medx: float = 35.0  # + for compression on top flange
        self.Medy: float = 0.20  # + for compression on web
        self.Vedy: float = 12.0  # Shear along web
        self.Vedx: float = 0.00  # Shear along flanges
