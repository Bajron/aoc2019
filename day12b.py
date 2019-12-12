#!/usr/bin/env python3
import math

from  collections import namedtuple
Moon = namedtuple('Moon',['x','y','z'])

moons = [
    Moon(x=5, y=13, z=-3),
    Moon(x=18, y=-7, z=13),
    Moon(x=16, y=3, z=4),
    Moon(x=0, y=8, z=8),
]

test_moons = [
    Moon(x=-1, y=0, z=2),
    Moon(x=2, y=-10, z=-7),
    Moon(x=4, y=-8, z=8),
    Moon(x=3, y=5, z=-1),
]

test_moons_big = [
    Moon(x=-8, y=-10, z=0),
    Moon(x=5, y=5, z=10),
    Moon(x=2, y=-7, z=3),
    Moon(x=9, y=-8, z=-3),
]

def signum(n):
    if n == 0: return 0
    if n < 0: return -1
    return 1

def energy(moon):
    s = 0
    for c in range(3):
        s += abs(moon[c])
    return s

def add(m1, m2):
    m = [0,0,0]
    for c in range(3):
        m[c] = m1[c] + m2[c]
    return m

def sub(m1, m2):
    m = [0,0,0]
    for c in range(3):
        m[c] = m1[c] - m2[c]
    return m

def calculateGravity(moons):
    gravity = [[0,0,0]] * len(moons)

    for i in range(len(moons)):
        for j in range(i+1, len(moons)):
            m1 = moons[i]
            m2 = moons[j]
            change = []
            for c in range(3):
                s = signum(m2[c] - m1[c])
                change.append(s)
            gravity[i] = add(gravity[i], change)
            gravity[j] = sub(gravity[j], change)
    return gravity

def applyTensorChange(velocity, gravity):
    for i in range(len(velocity)):
        velocity[i] = add(velocity[i], gravity[i])
    return velocity

# moons = test_moons_big
moons = [list(m) for m in moons]
velocity = [[0,0,0]] * len(moons)

def processCoordinates(coord):
    v = [0]*len(coord)
    initial = coord.copy()
    iteration = 0
    while True:
        g = [0] * len(coord)
        for i in range(len(coord)):
            for j in range(i+1, len(coord)):
                s = signum(coord[j] - coord[i])
                g[i] = g[i] + s
                g[j] = g[j] - s
        for i in range(len(coord)):
            v[i] = v[i] + g[i]
            coord[i] = coord[i] + v[i]
        iteration += 1
        cycled = True
        for i in range(len(coord)):
            if coord[i] != initial[i] or v[i] != 0:
                cycled = False
                break
        if cycled:
            break
        
    return iteration

# each coordinate separately?
x = processCoordinates([c[0] for c in moons])
y = processCoordinates([c[1] for c in moons])
z = processCoordinates([c[2] for c in moons])
print('x:', x)
print('y:', y)
print('z:', z)

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

print(lcm(lcm(x,y), z))

