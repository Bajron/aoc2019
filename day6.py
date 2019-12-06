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

depth = defaultdict(lambda : 0)

def walk_depth(node, d=0):
    global depth, neighbor
    depth[node] = d
    for ch in neighbor[node]:
        walk_depth(ch, d=d+1)

for n in nodes:
    if not parents[n]:
        walk_depth(n)

print(sum(depth.values()))