#!/usr/bin/env python3
import sys

def fuel_requirement(mass):
    step = mass // 3 - 2
    if step > 0:
        return step + fuel_requirement(step)
    return 0

lines = sys.stdin.readlines()
data = [int(l.strip()) for l in lines]

requirements = [ fuel_requirement(d) for d in data]
print(sum(requirements))