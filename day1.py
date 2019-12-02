#!/usr/bin/env python3
import sys

lines = sys.stdin.readlines()
data = [int(l.strip()) for l in lines]

requirements = [ (d//3 - 2) for d in data]
print(sum(requirements))