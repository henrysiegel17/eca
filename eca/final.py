'''''
GIVEN ANY BOARD POSITION WITH AN ARBITRARY NUMBER OF PAIRS OF KNIGHTS, 
THE GOAL IS TO SWITCH THE POSITIONS OF THE WHITE AND BLACK KNIGHTS


'''''

import heurestic
import updated_heuristic

# determines how to partition the grid up into smaller groups of knights


def copy2Darray(A):
    c = []
    for i in range(len(A)):
        row = []
        for j in range(len(A[i])):
            row.append(A[i][j])
        c.append(row)
    return c

def getMinimum(numbers):
    min = numbers[0]
    for i in range(len(numbers)):
        if numbers[i] < min:
            min = numbers[i]
    return min

def main():
    board4 = [
    ["Y", "Y", "B", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "W", "Y", "Y"],
    ["Y", "Y", "Y", "B", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "B", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["B", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "W", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "W", "W", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "B", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["W", "Y", "Y", "B", "W", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ]

    board5 = [
    ["Y", "Y", "B", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "B", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "W", "W", "W", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "W", "W", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "B", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "B", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["B", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ]

    board1 = [
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "N", "Y", "Y", "N", "Y", "Y", "Y"],
    ["Y", "N", "N", "N", "N", "N", "N", "Y", "B"],
    ["N", "Y", "N", "N", "N", "N", "N", "Y", "Y"],
    ["N", "N", "N", "N", "N", "N", "N", "N", "N"],
    ["N", "N", "Y", "N", "N", "N", "N", "N", "N"],
    ["Y", "Y", "Y", "N", "N", "Y", "N", "Y", "Y"],
    ["Y", "Y", "Y", "B", "Y", "Y", "N", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "W", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "N", "N", "N", "Y", "Y"],
    ["W", "Y", "Y", "B", "N", "N", "N", "W", "Y"]
    ]


    board = [
    ["B", "B", "B", "B", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "Y", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "Y", "N", "N"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "N", "N"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "N", "N", "N", "N", "Y", "Y", "Y"],
    ["N", "Y", "Y", "Y", "Y", "N", "Y", "Y", "Y"],
    ["N", "Y", "Y", "N", "N", "N", "Y", "Y", "Y"],
    ["W", "W", "W", "W", "Y", "Y", "Y", "Y", "Y"],
]

    board8 = [
    ["B", "Y", "Y", "Y", "Y", "Y", "B", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "B", "B", "Y", "Y", "Y", "Y", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "Y", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "Y", "N", "N"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "N", "N"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "N", "N", "N", "N", "Y", "Y", "Y"],
    ["N", "Y", "Y", "Y", "Y", "N", "Y", "Y", "Y"],
    ["W", "Y", "Y", "N", "N", "N", "Y", "Y", "Y"],
    ["W", "W", "W", "Y", "Y", "Y", "Y", "Y", "Y"],
]


    board3 = [
    ["B", "B", "B", "B", "Y", "Y", "Y", "Y", "Y"],
    ["B", "B", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["W", "W", "W", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["W", "W", "Y", "Y", "Y", "W", "Y", "Y", "Y"],
    ]

    board7 = [
        ["N", "N", "N", "Y", "Y", "Y", "Y"],
        ["Y", "Y", "Y", "Y", "N", "N", "Y"],
        ["Y", "Y", "Y", "N", "N", "N", "Y"],
        ["B", "B", "W", "W", "N", "N", "Y"],
        ["B", "B", "W", "W", "Y", "Y", "Y"]
    ]

    board2 = [
        ["N", "W", "N", "N"],
        ["N", "Y", "Y", "N"],
        ["N", "Y", "W", "Y"],
        ["B", "Y", "B", "Y"],
    ]

    board9 = [
        ["N", "W", "Y", "N"],
        ["N", "Y", "Y", "N"],
        ["N", "Y", "W", "Y"],
        ["B", "Y", "B", "Y"],
        ["W", "Y", "Y", "B"]
    ]

    board10 = [
    ["B", "Y", "N", "N", "N", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "N", "Y", "N", "N", "Y", "B", "Y"],
    ["Y", "Y", "N", "Y", "N", "N", "Y", "Y", "Y"],
    ["Y", "N", "Y", "Y", "N", "N", "N", "Y", "Y"],
    ["Y", "N", "Y", "Y", "N", "N", "N", "N", "B"],
    ["Y", "B", "B", "N", "N", "Y", "N", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "N", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "Y", "N", "N"],
    ["Y", "N", "N", "Y", "Y", "Y", "Y", "N", "N"],
    ["N", "N", "N", "Y", "Y", "Y", "Y", "N", "N"],
    ["N", "N", "Y", "Y", "Y", "Y", "Y", "N", "N"],
    ["N", "N", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "N", "N", "N", "N", "N", "N", "Y", "N"],
    ["N", "N", "Y", "Y", "Y", "N", "N", "Y", "Y"],
    ["N", "W", "N", "N", "N", "N", "N", "N", "Y"],
    ["N", "W", "W", "N", "Y", "Y", "Y", "W", "W"],
]

    board11 = [
    ["B", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "W"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "W", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "B", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["W", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "B"],
    ]

    board12 = [
        ["Y", "Y", "Y", "Y", "Y", "Y", "Y"],
        ["Y", "Y", "Y", "Y", "Y", "N", "Y"],
        ["Y", "Y", "Y", "Y", "N", "N", "Y"],
        ["Y", "Y", "Y", "N", "N", "N", "Y"],
        ["N", "N", "N", "N", "Y", "Y", "Y"],
        ["N", "N", "N", "Y", "Y", "Y", "Y"],
        ["N", "N", "N", "N", "N", "Y", "Y"],
        ["N", "N", "N", "N", "N", "Y", "Y"],
        ["B", "B", "W", "W", "Y", "Y", "Y"],
        ["B", "B", "W", "W", "Y", "Y", "Y"]
    ]
    
    board13 = [
    ["Y", "B", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "Y", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "Y", "N", "N"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "N", "N"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "N", "N", "N", "N", "Y", "Y", "Y"],
    ["N", "Y", "Y", "Y", "Y", "N", "Y", "Y", "Y"],
    ["N", "Y", "Y", "N", "N", "N", "Y", "Y", "Y"],
    ["Y", "Y", "W", "Y", "Y", "Y", "Y", "Y", "Y"],
]

    board14 = [
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "N", "N", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "N", "N", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "N", "N", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "N", "N", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "N", "N", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "N", "N", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "N", "N", "Y", "Y"],
    ["N", "N", "N", "N", "N", "N", "N", "Y", "Y"],
    ["N", "N", "N", "N", "N", "N", "N", "Y", "Y"],
    ["B", "B", "W", "W", "Y", "Y", "Y", "Y", "Y"],
    ["B", "B", "W", "W", "Y", "Y", "Y", "Y", "N"],
]

    board6 = [
    ["B", "B", "B", "B", "Y", "Y", "Y", "Y", "Y"],
    ["B", "B", "B", "B", "B", "B", "Y", "Y", "Y"],
    ["B", "B", "B", "B", "B", "B", "B", "Y", "Y"],
    ["B", "B", "B", "B", "B", "B", "Y", "Y", "Y"],
    ["W", "W", "W", "W", "W", "W", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["B", "B", "B", "B", "B", "B", "Y", "Y", "Y"],
    ["W", "W", "W", "W", "W", "W", "Y", "Y", "Y"],
    ["W", "W", "W", "W", "W", "W", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "W", "W", "W", "W"],
    ["W", "W", "W", "W", "W", "W", "W", "Y", "Y"],
    ]

    board15 = [
    ["W", "Y", "N", "N", "N", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "N", "Y", "N", "N", "Y", "B", "Y"],
    ["Y", "Y", "N", "Y", "N", "N", "Y", "Y", "Y"],
    ["Y", "N", "Y", "Y", "N", "N", "N", "Y", "Y"],
    ["Y", "N", "Y", "Y", "N", "N", "N", "N", "B"],
    ["Y", "B", "W", "N", "N", "Y", "N", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "N", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "Y", "N", "N"],
    ["Y", "N", "N", "Y", "Y", "Y", "Y", "N", "N"],
    ["N", "N", "N", "Y", "Y", "Y", "Y", "N", "N"],
    ["N", "N", "Y", "Y", "Y", "Y", "Y", "N", "N"],
    ["N", "N", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "N", "N", "N", "N", "N", "N", "Y", "N"],
    ["N", "N", "Y", "Y", "Y", "N", "N", "Y", "Y"],
    ["N", "W", "N", "N", "N", "N", "N", "N", "Y"],
    ["N", "B", "W", "N", "Y", "Y", "Y", "W", "B"],
]

    board16 = [
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "N", "N", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "N", "N", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "N", "N", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "N", "N", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "N", "N", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "N", "N", "Y", "Y"],
    ["N", "N", "N", "N", "N", "N", "N", "Y", "Y"],
    ["N", "N", "N", "N", "N", "N", "N", "N", "Y"],
    ["B", "B", "B", "W", "W", "W", "N", "N", "Y"],
    ["B", "B", "B", "W", "W", "W", "Y", "Y", "Y"],
    ["B", "B", "B", "W", "W", "W", "Y", "Y", "Y"],
]

    board17 = [
    ["N", "N", "N", "N", "N", "N", "N", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "N", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "N", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "N", "Y", "N"],
    ["N", "N", "N", "N", "N", "N", "N", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "N", "N", "Y"],
    ["N", "B", "B", "B", "W", "W", "W", "N", "N"],
    ["N", "B", "B", "B", "W", "W", "W", "N", "N"],
    ["N", "B", "B", "B", "W", "W", "W", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "N", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "N", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "N", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "N", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "N", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "N", "N", "N"],
]

    board18 = [
    ["Y", "B", "B", "B", "W", "W", "W"],
    ["Y", "B", "B", "B", "W", "W", "W"],
    ["Y", "B", "B", "Y", "Y", "W", "W"],
    ["Y", "B", "B", "Y", "Y", "W", "W"],
    ["Y", "B", "B", "B", "W", "W", "W"]
]

    board19 = [
    ["N", "N", "N", "N", "N", "N", "N", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "N", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "N", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "N", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "N", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "N", "N", "N"],
    ["N", "B", "B", "B", "W", "W", "W", "N", "Y"],
    ["N", "B", "B", "B", "W", "W", "W", "N", "N"],
    ["N", "B", "B", "B", "W", "W", "W", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "N", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "N", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "N", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "N", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "N", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "N", "N", "N"],
]

    board20 = [
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "N", "N", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "N", "N", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "N", "N", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "N", "N", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "N", "N", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "N", "N", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "N", "N", "Y", "Y"],
    ["N", "N", "N", "N", "N", "N", "N", "Y", "Y"],
    ["N", "N", "N", "N", "N", "N", "N", "W", "W"],
    ["B", "B", "B", "B", "B", "W", "W", "W", "W"],
    ["B", "B", "B", "B", "B", "W", "W", "W", "W"],
]



    small_limit = 3000
    big_limit = 10
    p_size_limit = 10
    rand_limit = 1000
    updated_heuristic.updated_hueristic(board20, small_limit, big_limit, p_size_limit, rand_limit)
    
if "__main__" == __name__:
    main()