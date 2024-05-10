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
        self.main()

    def main(self):
        # Main inputs for the calculations:
        # ==== Sections ====
        self.A: float = 150.0
        self.B: float = 47.0
        self.C: float = 16.0
        self.t: float = 1.0
        self.R: float = 3.0
        # ==== Material ====
        self.MatName: str = 'S350'
        self.fy: float = 350.0
        self.fu: float = 420.0
        # ==== Member ====
        self.Lx = 3000.0
        self.Ly = 3000.0
        self.Lt = 3000.0
        self.C1 = 1.127

