#!/usr/bin/env python

import sys
from collections import namedtuple

Direction=namedtuple('Direction', ['direction', 'distance'])

def process_input(input):
    return [Direction(direction=e[0], distance=int(e[1:])) for e in input.split(',')]

wire1_directions = process_input(sys.stdin.readline())
wire2_directions = process_input(sys.stdin.readline())

W,H = 10000,10000
canvas_1 = [ [-1]*(2*W) for _ in range(2*H)]
canvas_2 = [ [-1]*(2*W) for _ in range(2*H)]
sections = []

def fill(canvas, x, y, value):
    canvas[y+W][x+H] = value

def get(canvas, x, y):
    return canvas[y+W][x+H]

def walk_from_zero(directions, step_action):
    x,y = 0,0
    step = 0
    step_action(x,y,step)

    for d in directions:
        if d.direction == 'U':
            for yy in range(y + 1, y + d.distance + 1, 1):
                y = yy
                step += 1
                step_action(x,y,step)
        elif d.direction == 'D':
            for yy in range(y - 1, y - d.distance - 1, -1):
                y = yy
                step += 1
                step_action(x,y,step)
        elif d.direction == 'L':
            for xx in range(x - 1, x - d.distance - 1, -1):
                x = xx
                step += 1
                step_action(x,y,step)
        elif d.direction == 'R':
            for xx in range(x + 1, x + d.distance + 1, 1):
                x = xx
                step += 1
                step_action(x,y,step)

def w1_action(x,y,step):
    if get(canvas_1, x, y) == -1:
        fill(canvas_1, x, y, step)


def w2_action(x,y,step):
    c2 = get(canvas_2, x, y)
    if c2 == -1:
        fill(canvas_2, x, y, step)
        c2 = step

    c1 = get(canvas_1, x, y)
    if c1 > 0 and c2 > 0:
        print ('section',x,y,c1,c2)
        sections.append((x,y,c1,c2))

walk_from_zero(wire1_directions, w1_action)
walk_from_zero(wire2_directions, w2_action)

min_measure = 1000000
for s in sections:
    ss = s[2] + s[3]
    if not(s[0] == 0 and s[1] == 0) and ss < min_measure:
        min_measure = ss

print(min_measure)