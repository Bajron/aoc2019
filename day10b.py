#!/usr/bin/env python3

import sys
import collections
import math

data = [line.strip() for line in sys.stdin.readlines()]

asteroids = []
for y in range(len(data)):
    for x in range(len(data[y])):
        if data[y][x] == '#':
            asteroids.append((x,-y))


inSightOfNode = []
for i in range(len(asteroids)):
    a = asteroids[i]
    inSight = collections.defaultdict(lambda : [])
    for j in range(len(asteroids)):
        if j == i:
            continue
        b = asteroids[j]
        yy, xx = b[1] - a[1], b[0] - a[0]

        ang = math.atan2(yy, xx)
        ang -= math.pi / 2
        if ang < 0:
            ang += math.pi * 2
        
        inSight[ang].append(b)
    inSightOfNode.append(inSight)

maxInSight = 0
maxNode = None
for i in range(len(asteroids)):
    x = len(inSightOfNode[i].keys())
    if x > maxInSight:
        maxInSight = x
        maxNode = i

print(inSightOfNode[maxNode].keys())
print('Max in sight is', maxInSight, 'for node', maxNode,'that is', asteroids[maxNode])

angles = list(inSightOfNode[maxNode].keys())
angles.sort()

if angles[0] == 0.0:
    i = 0
else:
    i = len(angles[-1])

def dist(other):
    x = other[0] - asteroids[maxNode][0]
    y = other[1] - asteroids[maxNode][1]
    return  x*x + y*y

for ang in angles:
    inSightOfNode[maxNode][ang].sort(key=dist)

look_for = 200
for k in range(look_for - 1):
    while not len(inSightOfNode[maxNode][angles[i]]) > 0:
        i -= 1
        if i < 0:
            i += len(angles)

    onLine = inSightOfNode[maxNode][angles[i]]
    print ('Vaporizing',k, 'at',onLine[0])
    inSightOfNode[maxNode][angles[i]] = onLine[1:]
    i -= 1
    if i < 0:
        i += len(angles)

# Align for the last one to delete
while not len(inSightOfNode[maxNode][angles[i]]) > 0:
        i -= 1
        if i < 0:
            i += len(angles)

onLine = inSightOfNode[maxNode][angles[i]]
print('To vaporize', onLine[0])

print('WARNING: y coordinate is flipped, apply -y on your own!')