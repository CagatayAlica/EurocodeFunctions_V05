liste = ([['AXIAL', 'local', 0.225352617150792, 78.8734160027772], ['AXIAL', 'distortional', 0.3577012995831703, 125.19545485410961]],
         [['BENDING', 'local', 1.1606687104645228, 406.234048662583], ['BENDING', 'distortional', 0.9243055744346, 323.50695105211]])


def effective(res):
    f_crit = None
    for group in res:
        for mode in group:
            if mode[0] == 'AXIAL' and mode[1] == 'distortional':
                f_crit = mode[3]
                break

    # Place error check OUTSIDE the loop after searching all modes
    if f_crit is None:
        raise ValueError("f_crit is None. Ensure BucklingResults calculated a valid critical stress.")

    return f_crit


ff = effective(liste)
print(ff)  # Outputs: 125.19545485410961