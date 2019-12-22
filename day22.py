#!/usr/bin/env python3

import sys
import itertools

# cut 2257
# deal with increment 18
# cut -7620
# deal with increment 13
# cut 2616
# deal into new stack

orders = sys.stdin.readlines()

size = 10
size = 10007
state = list(range(size))
stateSwap = [0]*len(state)

for o in orders:
    # print(state)
    if o.startswith('cut '):
        i = int(o.split(' ')[1])
        state = state[i:] + state[:i]
    elif o.startswith('deal into new stack'):
        state.reverse()
    elif o.startswith('deal with increment'):
        inc = int(o.split(' ')[3])
        put = 0
        i = 0
        while put != len(state):
            stateSwap[i] = state[put]
            i = (i + inc) % size
            put += 1
        state, stateSwap = stateSwap, state

print(state[:20])
print(state.index(2019))