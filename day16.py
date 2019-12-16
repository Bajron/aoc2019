#!/usr/bin/env python3

import sys
import collections
import math

inputString = sys.stdin.read().strip()

offset = int(inputString[:7], base=10)
numbers = [int(x) for x in inputString] * 10000

baseRep = [0,1,0,-1]
reps = []
for i in range(len(numbers)):
    rep = []
    for e in baseRep:
        rep.extend([e] * (i+1))
    reps.append(rep)

print('Prepared extensions')

for i in range(100):
    for j in range(len(numbers)):
        rep = reps[j]
        lr = len(rep)
        s = 0
        for k in range(len(numbers)):
            s += numbers[k] * rep[(k + 1) % lr]
        numbers[j] = abs(s) % 10
    print('Iteration', i, 'done')

output = ''.join(str(x) for x in numbers)

print('From', inputString)
print('First 8', output[:8])
print('Last 8', output[-8:])
print('Offset is', offset)
print('Message ', output[offset:offset+8])