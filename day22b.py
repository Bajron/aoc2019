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

shuffleTimes = 101741582076661

size         = 119315717514047
position = 2020

# answer from part 1, for 2019
#size = 10007
# position = 4703

#size = 16063   

positionSet = set()
positionSequence = []
iteration = 0
while position not in positionSet:
    positionSet.add(position)
    positionSequence.append(position)

    for o in reversed(orders):
        if o.startswith('cut '):
            i = int(o.split(' ')[1])
            if i > 0:
                left = i
                right = size - i
            else:
                left = size - -i
                right = -i
            
            # reverse resulting position
            if position < right:
                # positions after move was on left side, so before it was on the right side
                position = left + position
            else:
                # position after move was on right side, so before it was on the left side
                position = position - right

            #state = state[i:] + state[:i]
        elif o.startswith('deal into new stack'):
            position = size - 1 - position
            #state.reverse()
        elif o.startswith('deal with increment'):
            inc = int(o.split(' ')[3])
            
            # hope the size is prime
            incModInverse = pow(inc, size - 2, size)
            #  k * inc = pos            mod size
            #  k = pos * incModInverse  mod size

            position = (position * incModInverse) % size

            # put = 0
            # i = 0
            # while put != len(state):
            #     stateSwap[i] = state[put]
            #     i = (i + inc) % size
            #     put += 1
            # state, stateSwap = stateSwap, state
    
    #print('Iteration', iteration)
    iteration += 1
    if iteration % 10000 == 0:
        print('Iteration', iteration)
        sys.stdout.flush()

print('Iteration', iteration)
print(positionSequence)

# for i in range(len(positionSequence)):
#     print(positionSequence[i] - positionSequence[(i-1)%len(positionSequence)])

print('Cycle length', len(positionSequence))
print('Original position', position)

# something probably needs to be reversed, but it does not matter, because this approach sucks
print ('Guessed value', positionSequence[shuffleTimes % len(positionSequence)])