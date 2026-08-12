import math
import numpy as np
import pandas as pd
import Constants.Constants as cons
import Main


class SolvePurlins:
    def __init__(self):
        self.Eds = None
        self.Report = None

        ang = 18.0  # Roof angle in degrees.
        spa = 610.0  # mm Purlin spacing.
        length = 1560.0  # mm Purlin span.

        # ==== Loads
        Dr = 0.60  # kPa
        Dc = 0.00  # kPa
        S = 0.924  # kPa
        W1 = 0.937  # kPa (Compression)
        W2 = -1.499  # kPa (Suction)
        Rl = 1.0  # kN
        AngleCos = math.cos(math.radians(ang))
        # ==== Uniform Loads
        wdr = Dr * (spa / 1000) * AngleCos
        wdc = Dc * (spa / 1000) * AngleCos
        ws = S * (spa / 1000) * AngleCos
        ww1 = W1 * (spa / 1000)
        ww2 = W2 * (spa / 1000)

        Rep = f'{cons.secDivider}\nDESIGN LOADS\n{cons.secDivider}\n'
        Rep += f'{Dr:.2f} kPa, dead load on roof.\n'
        Rep += f'{Dc:.2f} kPa, dead load on ceiling.\n'
        Rep += f'{S:.2f} kPa, snow load on roof.\n'
        Rep += f'{W1:.2f} kPa, wind pressure on roof surface creates compression.\n'
        Rep += f'{-W2:.2f} kPa, wind pressure on roof surface creates suction.\n'

        Rep += f'{cons.secDivider}\nUNIFORM LOAD on PURLIN\n{cons.secDivider}\n'
        Rep += f'wdr, {wdr:.2f} kN/m, dead load on roof.\n'
        Rep += f'wdc, {wdc:.2f} kN/m, dead load on ceiling.\n'
        Rep += f'ws, {ws:.2f} kN/m, snow load on roof.\n'
        Rep += f'ww1, {ww1:.2f} kN/m, wind pressure on roof surface creates compression.\n'
        Rep += f'ww2, {ww2:.2f} kN/m, wind pressure on roof surface creates suction.\n'

        Rep += f'{cons.secDivider}\nEUROCODE COMBINATIONS\n{cons.secDivider}\n'
        Loads = {'STR1': {'uniform': 1.35 * wdr + 1.35 * wdc, 'point': 0.0},
                 'STR2': {'uniform': 1.35 * wdr + 1.35 * wdc + 1.50 * ws, 'point': 0.0},
                 'STR3': {'uniform': 1.35 * wdr + 1.35 * wdc + 1.50 * ww1, 'point': 0.0},
                 'STR4': {'uniform': 1.35 * wdr + 1.35 * wdc + 1.50 * ww2, 'point': 0.0},
                 'STR5': {'uniform': 1.35 * wdr + 1.35 * wdc + 1.50 * ws + 1.50 * 0.6 * ww1, 'point': 0.0},
                 'STR6': {'uniform': 1.35 * wdr + 1.35 * wdc + 1.50 * ws + 1.50 * 0.6 * ww2, 'point': 0.0},
                 'STR7': {'uniform': 1.35 * wdr + 1.35 * wdc + 1.50 * ww1 + 1.50 * 0.7 * ws, 'point': 0.0},
                 'STR8': {'uniform': 1.35 * wdr + 1.35 * wdc + 1.50 * ww2 + 1.50 * 0.7 * ws, 'point': 0.0},
                 'STR9': {'uniform': 1.35 * wdr + 1.35 * wdc, 'point': 1.50 * Rl},
                 'STR10': {'uniform': 1.35 * wdr + 1.35 * wdc + 1.50 * 0.7 * ws, 'point': 1.50 * Rl},

                 'SERV1': {'uniform': 1.00 * wdr + 1.00 * wdc, 'point': 0.0},
                 'SERV2': {'uniform': 1.00 * wdr + 1.00 * wdc + 1.00 * ws, 'point': 0.0},
                 'SERV3': {'uniform': 1.00 * wdr + 1.00 * wdc + 1.00 * ww1, 'point': 0.0},
                 'SERV4': {'uniform': 1.00 * wdr + 1.00 * wdc + 1.00 * ww2, 'point': 0.0},
                 'SERV5': {'uniform': 1.00 * wdr + 1.00 * wdc + 1.00 * ws + 1.00 * 0.6 * ww1, 'point': 0.0},
                 'SERV6': {'uniform': 1.00 * wdr + 1.00 * wdc + 1.00 * ws + 1.00 * 0.6 * ww2, 'point': 0.0},
                 'SERV7': {'uniform': 1.00 * wdr + 1.00 * wdc + 1.00 * ww1 + 1.00 * 0.7 * ws, 'point': 0.0},
                 'SERV8': {'uniform': 1.00 * wdr + 1.00 * wdc + 1.00 * ww2 + 1.00 * 0.7 * ws, 'point': 0.0},
                 'SERV9': {'uniform': 1.00 * wdr + 1.00 * wdc, 'point': 1.00 * Rl},
                 'SERV10': {'uniform': 1.00 * wdr + 1.00 * wdc + 1.00 * 0.7 * ws, 'point': 1.00 * Rl}
                 }

        Rep += f'STR1 = 1.35 * wdr + 1.35 * wdc = \n{cons.sp9}1.35 * {wdr:.2f} + 1.35 * {wdc:.2f} = {Loads["STR1"]["uniform"]:.2f} kN/m\n'
        Rep += f'STR2 = 1.35 * wdr + 1.35 * wdc + 1.50 * ws = \n{cons.sp9}1.35 * {wdr:.2f} + 1.35 * {wdc:.2f} + 1.50 * {ws:.2f} = {Loads["STR2"]["uniform"]:.2f} kN/m\n'
        Rep += f'STR3 = 1.35 * wdr + 1.35 * wdc + 1.50 * ww1 = \n{cons.sp9}1.35 * {wdr:.2f} + 1.35 * {wdc:.2f} + 1.50 * {ww1:.2f} = {Loads["STR3"]["uniform"]:.2f} kN/m\n'
        Rep += f'STR4 = 1.35 * wdr + 1.35 * wdc + 1.50 * ww2 = \n{cons.sp9}1.35 * {wdr:.2f} + 1.35 * {wdc:.2f} + 1.50 * {ww2:.2f} = {Loads["STR4"]["uniform"]:.2f} kN/m\n'
        Rep += f'STR5 = 1.35 * wdr + 1.35 * wdc + 1.50 * ws + 1.50 * 0.6 * ww1 = \n{cons.sp9}1.35 * {wdr:.2f} + 1.35 * {wdc:.2f} + 1.50 * {ws:.2f} + 1.50 * 0.6 * {ww1:.2f} = {Loads["STR5"]["uniform"]:.2f} kN/m\n'
        Rep += f'STR6 = 1.35 * wdr + 1.35 * wdc + 1.50 * ws + 1.50 * 0.6 * ww2 = \n{cons.sp9}1.35 * {wdr:.2f} + 1.35 * {wdc:.2f} + 1.50 * {ws:.2f} + 1.50 * 0.6 * {ww2:.2f} = {Loads["STR6"]["uniform"]:.2f} kN/m\n'
        Rep += f'STR7 = 1.35 * wdr + 1.35 * wdc + 1.50 * ww1 + 1.50 * 0.7 * ws = \n{cons.sp9}1.35 * {wdr:.2f} + 1.35 * {wdc:.2f} + 1.50 * {ww1:.2f} + 1.50 * 0.7 * {ws:.2f} = {Loads["STR7"]["uniform"]:.2f} kN/m\n'
        Rep += f'STR8 = 1.35 * wdr + 1.35 * wdc + 1.50 * ww2 + 1.50 * 0.7 * ws = \n{cons.sp9}1.35 * {wdr:.2f} + 1.35 * {wdc:.2f} + 1.50 * {ww2:.2f} + 1.50 * 0.7 * {ws:.2f} = {Loads["STR8"]["uniform"]:.2f} kN/m\n'
        Rep += f'STR9 = 1.35 * wdr + 1.35 * wdc  + 1.50 * Rl = \n{cons.sp9}1.35 * {wdr:.2f} + 1.35 * {wdc:.2f} = {Loads["STR9"]["uniform"]:.2} kN/m, 1.50 * {Rl:.2f} = {Loads["STR9"]["point"]:.2f} kN on midpoint\n'
        Rep += f'STR10 = 1.35 * wdr + 1.35 * wdc + 1.50 * 0.7 * ws + 1.50 * Rl = \n{cons.sp9}1.35 * {wdr:.2f} + 1.35 * {wdc:.2f} + 1.50 * 0.7 * {ws:.2f} = {Loads["STR9"]["uniform"]:.2} kN/m, 1.50 * {Rl:.2f} = {Loads["STR9"]["point"]:.2f} kN on midpoint\n'
        self.Eds = []
        Rep += f'{cons.secDivider}\nPURLIN\n{cons.secDivider}\n'
        Rep += f'{length:.2f} mm purlin span.\n'
        Rep += f'{spa:.2f} mm purlin spacings.\n'
        Rep += f'{ang:.2f} degrees roof angle.\n'
        for key, value in Loads.items():
            N: float = 0.0
            Mx: float = value["uniform"] * math.pow(length / 1000, 2) / 8.0 + value["point"] * (length / 1000) / 4.
            Vy: float = value["uniform"] * length / 1000 / 2.
            My: float = 0.0
            Vx: float = 0.0
            self.Eds.append([key, f'{N:.3f}', f'{Mx:.3f}', f'{Vy:.3f}', f'{My:.3f}', f'{Vx:.3f}'])

            Rep += f'{key}, load : {value["uniform"]:.3f} kN/m, {value["point"]:.3f} kN at midpoint\n{cons.sp3}Med : {Mx:.3f} kN.m in midpoint\n{cons.sp3}Ved : {Vy:.3f} kN at supports.\n'

        Rep += f'{cons.secDivider}\nPURLIN\n{cons.secDivider}\n'
        Rep += f'{length:.2f} mm purlin span.\n'
        Rep += f'{spa:.2f} mm purlin spacings.\n'
        Rep += f'{ang:.2f} degrees roof angle.\n'
        self.Eds = np.array(self.Eds)
        self.df = pd.DataFrame(data=self.Eds,
                               columns=['Comb', 'N[kN]', 'Medx[kN.m]', 'Vedy[kN]', 'Medy[kN.m]', 'Vedx[kN]'])



        #pd.options.display.float_format = '{:,.2f}'.format

        self.Report = Rep


ss = SolvePurlins()
print(ss.Report)
pd.options.display.float_format = '{:,.2f}'.format
print(ss.df)
