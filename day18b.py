#!/usr/bin/env python3
import sys
import itertools
from collections import namedtuple, defaultdict

State=namedtuple('State', ['positions', 'cost', 'code'])

room = [l.strip() for l in sys.stdin.readlines()]

H = len(room)
W = len(room[0])

keys = ''.join([chr(x) for x in range(ord('a'), ord('z') + 1)])
realKeys = []
doors = keys.upper()
realDoors = []

for y in range(H):
    for x in range(W):
        ch = room[y][x]
        if ch == '@':
            start = (y,x)
        elif ch in keys:
            realKeys.append(ch)
        elif ch in doors:
            realDoors.append(ch)

room = [ list(x) for x in room ]

room[start[0]][start[1]] = '#'
room[start[0]-1][start[1]] = '#'
room[start[0]+1][start[1]] = '#'
room[start[0]][start[1]-1] = '#'
room[start[0]][start[1]+1] = '#'

s1 = (start[0]-1, start[1]-1)
room[start[0]-1][start[1]-1] = '@'

s2 = (start[0]+1, start[1]-1)
room[start[0]+1][start[1]-1] = '@'

s3 = (start[0]-1, start[1]+1)
room[start[0]-1][start[1]+1] = '@'

s4 = (start[0]+1, start[1]+1)
room[start[0]+1][start[1]+1] = '@'

room = [ ''.join(x) for x in room ]


initial = State((s1, s2, s3, s4), 0, '@')
print(initial)

for l in room:
    print(l)

def allKeysGathered(code):
    return all([ch in code for ch in realKeys])

def neigbors(pos):
    if len(pos) == 2:
        y,x = pos
    elif len(pos) == 3:
        y,x,_ = pos
    return [(y-1,x), (y+1,x),(y,x-1), (y,x+1)]
    
def neigborsForSet(pos):
    n = []
    for p in pos:
        nn = neigbors(p)
        nn.append(p)
        n.append(nn)
    
    return itertools.product(*n)

def getNextStates(state):
    visited = set()
    nextStates = []
    
    iteration = 1
    q = []
    q.extend(neigborsForSet(state.positions))
    visited.add(state.positions)

    while len(q) > 0:
        ql = len(q)
        for i in range(ql):
            positions = q[i]

            if positions in visited:
                continue

            visited.add(positions)

            badPosition = False
            for pos in positions:
                y, x = pos
                if x < 0 or x >= W or y < 0 or y >= H or room[y][x] == '#':
                    badPosition = True
                    break
            
            if badPosition:
                continue

            cannotMove = False
            addCode = ''
            for pos in positions:
                y, x = pos 
                ch = room[y][x]

                if ch in keys and not ch in state.code:
                    # aquired key
                    addCode += ch
                    createsState = True
                elif ch in doors and not ch in state.code:
                    if ch.lower() in state.code:
                        # opened door first time
                        addCode += ch
                        createsState = True
                    else:
                        # cutoff BFS (closed door)
                        cannotMove = True
            
            if cannotMove:
                continue

            if addCode:
                nextStates.append(State(positions, state.cost + iteration, state.code + addCode))
            else:
                 q.extend(neigborsForSet(positions))
            
        q = q[ql:]
        #print(iteration, 'done', ql, 'elements')
        sys.stdout.flush()
        iteration += 1

    return nextStates


prevStateCount = 0
states = [initial]
finalStates = []

bestAllKeys = 1000000000
bestAllKeysState = None

# while prevStateCount != len(states):
while len(states) > 0:
    print('States count', len(states))
    groups = defaultdict(lambda:[])
    for s in states:
        # same point, with same state so far
        
        l = list(s.code[:-1])
        l.sort()
        same = ''.join(l) + s.code[-1]
        groups[same].append(s)

        if allKeysGathered(s.code):
            if s.cost < bestAllKeys:
                bestAllKeys = s.cost
                bestAllKeysState = s

    states = []
    for k,v in groups.items():
        bestCost = 1000000000000
        for s in v:
            if s.cost < bestCost:
                bestCost = s.cost
        for s in v:
            if s.cost == bestCost:
                states.append(s)

    print('Filtered count', len(states))
    sys.stdout.flush()

    prevStateCount = len(states)
    nextStates = []
    for s in states:
        n = getNextStates(s)
        if n:
            nextStates.extend(n)
        else:
            finalStates.append(s)
    states = nextStates

    if len(states) < 50:
        print(states)
    

# not 6039

lowestCost = 1000000000000
bestState = None
for s in finalStates:
    if s.cost < lowestCost:
        lowestCost = s.cost
        bestState = s

print(bestState)
print(bestState.code)

print(bestAllKeys)
print(bestAllKeysState)