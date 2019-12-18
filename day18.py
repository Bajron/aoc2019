#!/usr/bin/env python3
import sys
from collections import namedtuple

State=namedtuple('State', ['position', 'cost', 'code'])

room = [l.strip() for l in sys.stdin.readlines()]

H = len(room)
W = len(room[0])

for y in range(H):
    for x in range(W):
        if room[y][x] == '@':
            start = (y,x)
            break

initial = State(start, 0, '')
print(initial)

keys = ''.join([chr(x) for x in range(ord('a'), ord('z') + 1)])
doors = keys.upper()

def neigbors(pos):
    y,x = pos
    return [(y-1,x), (y+1,x),(y,x-1), (y,x+1)]
    

def getNextStates(state):
    visited = [[False] * W for _ in range(H)]
    nextStates = []
    
    iteration = 1
    q = []
    q.extend(neigbors(state.position))

    while len(q) > 0:
        ql = len(q)
        for i in range(ql):
            pos = q[i]
            y, x = pos
            if x < 0 or x >= W or y < 0 or y >= H or visited[y][x] or room[y][x] == '#':
                continue
            visited[y][x] = True

            ch = room[y][x]

            if ch in keys and not ch in state.code:
                # aquired key
                nextStates.append(State(pos, state.cost + iteration, state.code + ch))
            elif ch in doors and not ch in state.code:
                if ch.lower() in state.code:
                    # opened door first time
                    nextStates.append(State(pos, state.cost + iteration, state.code + ch))
                # else cutoff BFS (closed door)
            else:
                # we move only when state was not changed
                q.extend(neigbors(pos))
        q = q[ql:]
        iteration += 1

    return nextStates


prevStateCount = 0
states = [initial]
finalStates = []

# while prevStateCount != len(states):
while len(states) > 0:
    print('States count', len(states))
    prevStateCount = len(states)
    nextStates = []
    for s in states:
        n = getNextStates(s)
        if n:
            nextStates.extend(n)
        else:
            finalStates.append(s)
    states = nextStates


lowestCost = 1000000000000
bestState = None
for s in finalStates:
    if s.cost < lowestCost:
        lowestCost = s.cost
        bestState = s

print(bestState)
print(bestState.code)