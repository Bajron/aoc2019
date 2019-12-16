#!/usr/bin/env python3

import sys
import collections
import math

inputString = sys.stdin.read().strip()

offset = int(inputString[:7], base=10)
numbers = [int(x) for x in inputString]*10000

baseRep = [0,1,0,-1]
baseRepLen = len(baseRep)

n = len(numbers)
print('Lenght of input', n)
print('After offset', n - offset)
for i in range(100):
    for j in range(offset-10, n):
        s = 0
        ri = 0
        k = j
        while k < n:
            if (k+1) % (j+1) == 0:
                ri += 1
                ri %= baseRepLen

                # we changed to zero, skip
                if baseRep[ri] == 0:
                    k += j+1
                    ri += 1
                if k >= n:
                    break

            s += numbers[k] * baseRep[ri]
            k += 1
        numbers[j] = abs(s) % 10

    print('Iteration', i, 'done')

output = ''.join(str(x) for x in numbers)

print('From', inputString)
print('Output', output)
print('First 8', output[:8])
print('Last 8', output[-8:])
print('Offset is', offset)
print('Message ', output[offset:offset+8])