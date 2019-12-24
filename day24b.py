#!/usr/bin/env python3

import sys
import copy
import collections

board = [x.strip() for x in sys.stdin.readlines()]

H = len(board)
W = len(board[0])

boardWithMargins = []
boardWithMargins.append(['.'] * (W + 2))
for l in board:
    boardWithMargins.append(['.'] + list(l) + ['.'])
boardWithMargins.append(['.'] * (W + 2))

bwm = boardWithMargins

def printBwm(bwm):
    for l in bwm:
        print(''.join(l))
    print(' -- ')

def neigbors(pos):
    y,x = pos
    return [(y-1,x), (y+1,x),(y,x-1), (y,x+1)]

def iteration(bwm, above, below):
    ret = copy.deepcopy(bwm)

    # modify outer region, notice! after initial copy
    # this margin is used only here, so modifying source is ok
    for x in range(1, W + 1):
        bwm[0][x] = above[2][3]
    for x in range(1, W + 1):
        bwm[6][x] = above[4][3]
    for y in range(1, H + 1):
        bwm[y][0] = above[3][2]
    for y in range(1, H + 1):
        bwm[y][6] = above[3][4]

    for y in range(1, H + 1):
        for x in range(1, W + 1):
            if y == 3 and x == 3:
                ret[y][x] = '?'
                continue

            bugs = 0
            for yy,xx in neigbors((y,x)):
                # neighbours of middle have some special cases
                if yy == 3 and xx == 3:
                    if y == 2:
                        for xxx in range(1, W+1):
                            if below[1][xxx] == '#':
                                bugs += 1
                    if y == 4:
                        for xxx in range(1, W+1):
                            if below[5][xxx] == '#':
                                bugs += 1
                    if x == 2:
                        for yyy in range(1, H+1):
                            if below[yyy][1] == '#':
                                bugs += 1
                    if x == 4:
                        for yyy in range(1, H+1):
                            if below[yyy][5] == '#':
                                bugs += 1
                elif bwm[yy][xx] == '#':
                    bugs += 1

            if bwm[y][x] == '#':
                if bugs != 1:
                    ret[y][x] = '.'
                    continue
            else:
                if bugs == 1 or bugs == 2:
                    ret[y][x] = '#'
                    continue

            ret[y][x] = bwm[y][x]
    return ret

def makeEmptyBwm():
    return [ ['.'] * (W+2) for _ in range(H+2)]

def countBugs(bwm):
    count = 0
    for y in range(1, H + 1):
        for x in range(1, W + 1):
            if bwm[y][x] == '#':
                count += 1
    return count

bwmAxis = collections.deque()
bwmAxis.append(bwm)
bwmAxis.append(makeEmptyBwm())
bwmAxis.appendleft(makeEmptyBwm())

for minute in range(200):
    bwmAxis.appendleft(makeEmptyBwm())
    bwmAxis.append(makeEmptyBwm())
    bwmAxisNext = copy.deepcopy(bwmAxis)
    for c in range(1, len(bwmAxis) - 1):
        bwmAxisNext[c] = iteration(bwmAxis[c], bwmAxis[c+1], bwmAxis[c-1])
    bwmAxis = bwmAxisNext

print('Middle after', minute, 'minutes')
printBwm(bwmAxis[len(bwmAxis) // 2])

count = 0
for bwm in bwmAxis:
    count += countBugs(bwm)

print('Total bugs', count)