import math
import pygame
"""
111
110
101
100
011
010
001
000
"""

YES = (225,67,67)
NO = (256,256,256)
WIDTH = 800
HEIGHT = 800

def eca(num, bitstring):
    values = converttoBinary(num, 8)
    rules = {
        "111": values[0],
        "110": values[1],
        "101": values[2],
        "100": values[3],
        "011": values[4],
        "010": values[5],
        "001": values[6],
        "000": values[7],
    }
    output = bitstring.copy()
    i = 0
    while i < len(bitstring):
        substring = (
            str(bitstring[(i - 1) % len(bitstring)])
            + str(bitstring[i % len(bitstring)])
            + str(bitstring[(i + 1) % len(bitstring)])
        )
        output[i] = rules.get(substring)
        i += 1
    return output


def eca_90(bitstring):
    output = bitstring.copy()
    i = 0
    while i < len(bitstring):
        if bitstring[(i - 1) % len(bitstring)] == bitstring[(i + 1) % len(bitstring)]:
            output[i] = 0
        else:
            output[i] = 1
        i += 1
    return output


def match(b1, b2):
    if len(b1) == len(b2):
        for i in range(0, len(b1)):
            if b1[i] != b2[i]:
                return False
        return True
    return False


def converttoBinary(num, size):
    remaining = num
    bitstring = []
    for s in range(0, size):
        bitstring.append(0)
    pow = size - 1
    while pow >= 0:
        if math.pow(2, pow) <= remaining:
            remaining = remaining - math.pow(2, pow)
            bitstring[len(bitstring) - 1 - pow] = 1
        pow -= 1
    return bitstring


def findfixedpoints(size):
    configurations = []
    for num in range(0, int(math.pow(2, size))):
        bitstring = converttoBinary(num, size)
        b1 = bitstring.copy()
        b2 = eca_90(bitstring).copy()
        if match(b1, b2) == True:
            configurations.append(bitstring)
    return configurations


def findfixedpointstep1(size):
    collection = []
    configurations = findfixedpoints(size)
    for num in range(0, int(math.pow(2, size))):
        bitstring = converttoBinary(num, size)
        f = eca_90(bitstring).copy()
        if f in configurations and match(f, bitstring) == False:
            collection.append(bitstring)
    return collection


configurations = findfixedpoints(9)
collection = findfixedpointstep1(9)
for i in range(0, len(configurations)):
    print(configurations[i])
for i in range(0, len(collection)):
    print(collection[i])
print(eca(89, [0, 0, 0, 0, 0, 0, 1]))

pygame.init()
# Initializing surface
surface = pygame.display.set_mode((WIDTH,HEIGHT))
size = 100
initial = []
initial = [0 for i in range(size)]
initial[int(size/2)] = 1
kth = initial.copy

#run n iterations of eca
n=100

for k in range(0,n):
    kth = eca(90,kth)
    for i in range(0,len(k)):
        color = YES
        if kth[i] == 0:
            color = NO
        pygame.draw.rect(surface, color, pygame.Rect(int(WIDTH/n*i), int(HEIGHT/n*k), int(WIDTH/n), int(HEIGHT/n)))
        pygame.display.flip()

