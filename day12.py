#!/usr/bin/env python3
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

for i in range(1000):
    if i % 10 == 0:
        print(i,'Moon 0', moons[0], velocity[0])

    gravity = calculateGravity(moons)
    print(gravity)
    velocity = applyTensorChange(velocity, gravity)
    moons = applyTensorChange(moons, velocity)

    if i%10 == 0:
        print(i,'Moon 0 energy', energy(moons[0]) * energy(velocity[0]))

total = 0
for i in range(len(moons)):
    total += energy(moons[i]) * energy(velocity[i])

print('Total:', total)