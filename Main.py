
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
        self.A: float = 100.0
        self.B: float = 44.0
        self.C: float = 10.0
        self.t: float = 1.2
        self.R: float = 1.6
        # ==== Material ====
        self.MatName: str = 'S280'
        self.fy: float = 280.0
        self.fu: float = 360.0
        # ==== Member ====
        self.Lx: float = 2800
        self.Ly: float = 1220
        self.Lt: float = 1220
        self.C1: float = 1.127
        # ==== Loads ====
        self.Ned: float = 10.614  # + for tension, - for compression
        self.Medx: float = 0.00  # + for compression on top flange
        self.Medy: float = 0.00  # + for compression on web
        self.Vedy: float = 0.00  # Shear along web
        self.Vedx: float = 0.00  # Shear along flanges

        secDivider = '============================================'
        Rep = f'{secDivider}\nUSER INPUT\n{secDivider}\n'
        Rep += f'==== Sections ====\n'
        Rep += f'A = {self.A:.2f} mm\n'
        Rep += f'B = {self.B:.2f} mm\n'
        Rep += f'C = {self.C:.2f} mm\n'
        Rep += f't = {self.t:.2f} mm\n'
        Rep += f'R = {self.R:.2f} mm\n'
        Rep += f'==== Material ====\n'
        Rep += f'Material = {self.MatName}\n'
        Rep += f'fy = {self.fy:.2f} MPa\n'
        Rep += f'fu = {self.fu:.2f} MPa\n'
        Rep += f'==== Member ====\n'
        Rep += f'Lx = {self.Lx:.2f} mm\n'
        Rep += f'Ly = {self.Ly:.2f} mm\n'
        Rep += f'Lt = {self.Lt:.2f} mm\n'
        Rep += f'C1 = {self.C1:.2f}\n'
        print(Rep)


def main():
    print("Hello World!")


if __name__ == "__main__":
    main()
