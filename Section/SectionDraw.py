import math
import numpy as np


def rotateCoordinates(XY, angle):
    # Shape of the input matrix
    num_rows, num_cols = XY.shape
    # Creating a dummy zeros matrix
    dummyzeros = np.zeros(num_cols)
    # Adding dummy zeros
    SectionWithZeros = np.vstack([XY, dummyzeros])
    # Cosine and sines
    c, s = np.cos(math.radians(angle)), np.sin(math.radians(angle))
    j = np.array([[c, s, 0],
                  [-s, c, 0],
                  [0, 0, 1]])
    # Multiply with transformation matrix
    RotatedCoordinates = np.matmul(j, SectionWithZeros)
    # Remove the dummy zeros
    RotatedCoordinates = np.delete(RotatedCoordinates, 2, 0)
    return XY, RotatedCoordinates


def ceeSection(A, B, C, t, angle):
    # C section input matrix is column1 is X column2 is Y coordinates.
    Csection = np.array([[B, C],
                         [B, 0],
                         [B / 2, 0],
                         [0, 0],
                         [0, (1.0 / 4.0) * A],
                         [0, (2.0 / 4.0) * A],
                         [0, (3.0 / 4.0) * A],
                         [0, (4.0 / 4.0) * A],
                         [B / 2, A],
                         [B, A],
                         [B, A - C]
                         ])
    # Function call for rotation
    Csection, RotatedCsection = rotateCoordinates(Csection.T, angle)
    # Create id numbers for each row
    numbers = np.arange(RotatedCsection.shape[1])

    # Adding id numbers to the coordinates matrix
    CsectionWithNumbers = np.vstack([numbers, RotatedCsection])

    # Creating ones
    ones = np.ones((4, RotatedCsection.shape[1]))
    # Adding one numbers to the coordinates matrix
    CsectionWithNumbers = np.vstack([CsectionWithNumbers, ones])
    # Creating zeros
    zeros = np.zeros((RotatedCsection.shape[1]))
    # Adding zeros to the coordinates matrix
    CsectionWithNumbers = np.vstack([CsectionWithNumbers, zeros])

    nodes = CsectionWithNumbers.T

    thickness = t
    elements = np.array([[0, 0, 1, thickness, 0],
                         [1, 1, 2, thickness, 0],
                         [2, 2, 3, thickness, 0],
                         [3, 3, 4, thickness, 0],
                         [4, 4, 5, thickness, 0],
                         [5, 5, 6, thickness, 0],
                         [6, 6, 7, thickness, 0],
                         [7, 7, 8, thickness, 0],
                         [8, 8, 9, thickness, 0],
                         [9, 9, 10, thickness, 0]
                         ])
    descp = "Section : A:" + str(A) + " B:" + str(B) + " C:" + str(C) + " t:" + str(t)
    return nodes, elements, thickness, descp




