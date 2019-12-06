#!/usr/bin/env python3
from collections import namedtuple, defaultdict
import sys

edges = [ x.strip().split(')') for x in sys.stdin.readlines()]

nodes = set()
parents = defaultdict(lambda : [])
# aka value orbits key
neighbor = defaultdict(lambda : [])
for e in edges:
    nodes.add(e[0])
    nodes.add(e[1])
    neighbor[e[0]].append(e[1])
    parents[e[1]].append(e[0])

san_visits = {}
you_visits = {}

def mark(visits, node, distance=0):
    global parents
    visits[node] = distance
    for p in parents[node]:
        mark(visits, p, distance=distance+1)

mark(san_visits, 'SAN')
mark(you_visits, 'YOU')

min = 1000000
node = None
for n in nodes:
    if n in san_visits and n in you_visits:
        s = san_visits[n] + you_visits[n]
        if s < min:
            min = s
            node = n

print(node)
print('sum:', min, ' sum-2:', min-2)