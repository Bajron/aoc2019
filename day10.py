#!/usr/bin/env python3

import sys
import collections
import math

data = [line.strip() for line in sys.stdin.readlines()]

asteroids = []
for y in range(len(data)):
    for x in range(len(data[y])):
        if data[y][x] == '#':
            asteroids.append((x,y))


inSightOfNode = []
for i in range(len(asteroids)):
    a = asteroids[i]
    inSight = collections.defaultdict(lambda : [])
    for j in range(len(asteroids)):
        if j == i:
            continue
        b = asteroids[j]
        yy, xx = b[0] - a[0], b[1] - a[1]
        inSight[math.atan2(yy, xx)].append(b)
    inSightOfNode.append(inSight)

maxInSight = 0
maxNode = None
for i in range(len(asteroids)):
    x = len(inSightOfNode[i].keys())
    if x > maxInSight:
        maxInSight = x
        maxNode = i

print('Max in sight is', maxInSight, 'for node', maxNode,'that is', asteroids[maxNode])
