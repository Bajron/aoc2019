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

producing = True

def acquire(resource, amount, state):
    global producing
    if resource == 'ORE':
        if producing:
            print('Want ORE', amount)
            state['ORE'] = state['ORE'] + amount
            return True
        else:
            if amount > state['ORE']:
                return False
            state['ORE'] = state['ORE'] - amount
            return True
    
    reaction = lookup[resource]

    need = amount - state[resource]

    if need > 0:
        runReaction = (need - 1) // reaction.output[0] + 1

        for deps in reaction.input:
            s = acquire(deps[1], deps[0] * runReaction, state)
            if not s:
                return False

        state[resource] = state[resource] + runReaction*reaction.output[0]

    state[resource] = state[resource] - amount
    return True


acquire('FUEL', 1, state)
orePerFuel = state['ORE']
print('ORE per fuel', orePerFuel)

producing = False
state = collections.defaultdict(lambda:0)
oreStart = 1000000000000
state['ORE'] = oreStart

fuel = oreStart // orePerFuel
ok = acquire('FUEL', oreStart // orePerFuel, state)
step = 1000
while step > 0:
    while True:
        stateBackup = state.copy()
        ok = acquire('FUEL', step, state)
        if not ok:
            state = stateBackup
            break
        else:
            fuel += step
    step = step // 2

while acquire('FUEL', 1, state):
        fuel += 1

print(state)
print('Got fuel:', fuel, state['FUEL'])
