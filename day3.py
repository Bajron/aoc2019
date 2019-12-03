#!/usr/bin/env python

import sys
from collections import namedtuple

Direction=namedtuple('Direction', ['direction', 'distance'])

def process_input(input):
    return [Direction(direction=e[0], distance=int(e[1:])) for e in input.split(',')]

wire1_directions = process_input(sys.stdin.readline())
wire2_directions = process_input(sys.stdin.readline())

def move_from_zero(directions):
    lines = []
    x,y = 0,0
    for d in directions:
        nx,ny = x,y
        if d.direction == 'U':
            ny += d.distance
        elif d.direction == 'D':
            ny -= d.distance
        elif d.direction == 'L':
            nx -= d.distance
        elif d.direction == 'R':
            nx += d.distance
        lines.append(((x,y), (nx, ny)))
        x,y = nx,ny
    
    return lines

def between(a,b,check):
    return (a <= check and check <= b) or (b <= check and check <= a)

# Watch out, this does not count for overlap
def cross(l1, l2):
    x1_0,y1_0 = l1[0]
    x1_1,y1_1 = l1[1]
    
    x2_0,y2_0 = l2[0]
    x2_1,y2_1 = l2[1]

    if x1_0 == x1_1 and y2_0 == y2_1:
        if between(x2_0, x2_1, x1_0) and between(y1_0, y1_1, y2_0):
            return (x1_0, y2_0)
    if x2_0 == x2_1 and y1_0 == y1_1:
        if between(x1_0, x1_1, x2_1) and between(y2_0, y2_1, y1_0):
            return (x2_1, y1_1)

    return None

w1 = move_from_zero(wire1_directions)
w2 = move_from_zero(wire2_directions)

print(w1)
print(w2)

sections = []
for i in range(len(w1)):
    for j in range(len(w2)):
        s = cross(w1[i], w2[j])
        if s: sections.append(s)

def dist(a,b): return abs(b[0] - a[0]) + abs(b[1] - a[1])

min_point = None
min_dist = 10000000

print('Sections', sections)

for s in sections:
    d = dist((0,0), s)
    if d > 0 and d < min_dist:
        min_dist = d
        min_point = s

print(min_point)
print(dist((0,0), min_point))