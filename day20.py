#!/usr/bin/env python3
import sys
import collections
room = [l.strip('\n\r') for l in sys.stdin.readlines()]

H = len(room)
W = len(room[0])

def neigbors(pos):
    y,x = pos
    return [(y-1,x), (y+1,x),(y,x-1), (y,x+1)]

def diff(source, destination):
    return (destination[0] - source[0], destination[1] - source[1])

def advance(source, delta):
    return (source[0] + delta[0], source[1] + delta[1])


letters = ''.join(chr(x) for x in range(ord('A'), ord('Z') + 1))
portals = collections.defaultdict(lambda : [])
for y in range(H):
    for x in range(W):
        if room[y][x] != '.': continue

        for yy,xx in neigbors((y,x)):
            if room[yy][xx] in letters:
                delta = diff((y,x), (yy,xx))
                another = advance((yy,xx), delta)

                adjecent = room[yy][xx] 
                following = room[another[0]][another[1]]
                if delta[1] == 1 or delta[0] == 1:
                    label = adjecent + following
                elif delta[1] == -1 or delta[0] == -1:
                    label = following + adjecent

                portals[label].append((y,x))

#print(portals)

portalsJumps = {}
for k,v in portals.items():
    if k == 'AA' or k == 'ZZ': continue
    portalsJumps[v[0]] = v[1]
    portalsJumps[v[1]] = v[0]

start = portals['AA'][0]
finish = portals['ZZ'][0]

print('Data parsed')

visited = [[False] * W for _ in range(H)]

iteration = 0
q = [start]
distance = None

while q and distance is None:
    ql = len(q)
    for i in range(ql):
        pos = q[i]
        y,x = pos
        
        if x < 0 or x >= W or y < 0 or y >= H or room[y][x] != '.' or visited[y][x]: continue
        
        visited[y][x] = True

        if pos == finish:
            distance = iteration
            break

        q.extend(neigbors(pos))
        if pos in portalsJumps:
            q.append(portalsJumps[pos])
    q = q[ql:]
    iteration += 1
print('Distance', distance)