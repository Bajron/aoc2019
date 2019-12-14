#!/usr/bin/env python3

import sys
import queue
import itertools
import collections

Reaction = collections.namedtuple('Reaction', ['input', 'output'])

lines = sys.stdin.readlines()
reactions = []
for l in lines:
    ft = [x.strip() for x in l.split('=>')]
    f = [tuple(y.strip().split(' ')) for y in ft[0].split(',')]
    f = [(int(x[0]), x[1]) for x in f]
    t = [tuple(y.strip().split(' ')) for y in ft[1].split(',')]
    t = [(int(x[0]), x[1]) for x in t]
    reactions.append(Reaction(f, t[0]))

lookup = {}
for r in reactions:
    lookup[r.output[1]] = r

state = collections.defaultdict(lambda:0)
state = collections.defaultdict(lambda:0)

def acquire(resource, amount, state):
    if resource == 'ORE':
        print('Want ORE', amount)
        state['ORE'] = state['ORE'] + amount
        return
    
    reaction = lookup[resource]

    need = amount - state[resource]
    runReaction = (need - 1) // reaction.output[0] + 1

    for deps in reaction.input:
        acquire(deps[1], deps[0] * runReaction, state)

    state[resource] = state[resource] + runReaction*reaction.output[0]
    state[resource] = state[resource] - amount

acquire('FUEL', 1, state)

print(state['ORE'])
print(state)
