#!/usr/bin/env python3

import sys
import copy

board = [x.strip() for x in sys.stdin.readlines()]

H = len(board)
W = len(board[0])

boardWithMargins = []
boardWithMargins.append(['.'] * (W + 2))
for l in board:
    boardWithMargins.append(['.'] + list(l) + ['.'])
boardWithMargins.append(['.'] * (W + 2))

bwm = boardWithMargins

def encodeBwm(bwm):
    p = 1
    r = 0
    for y in range(1, H + 1):
        for x in range(1, W + 1):
            if bwm[y][x] == '#':
                r += p
            p *= 2
    return r

def printBwm(bwm):
    for l in bwm:
        print(''.join(l))
    print(' -- ')

def neigbors(pos):
    y,x = pos
    return [(y-1,x), (y+1,x),(y,x-1), (y,x+1)]

def iteration(bwm):
    ret = copy.deepcopy(bwm)
    for y in range(1, H + 1):
        for x in range(1, W + 1):
            bugs = 0
            for yy,xx in neigbors((y,x)):
                if bwm[yy][xx] == '#':
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


code = encodeBwm(bwm)
codes = set()

while code not in codes:
    codes.add(code)
    printBwm(bwm)
    bwm = iteration(bwm)
    code = encodeBwm(bwm)

print('First repeating board code', code)
print(len(codes), 'codes in the set')
print('Final board')
printBwm(bwm)