#!/usr/bin/env python3

import sys

data = sys.stdin.read().strip()
print(data)

w = 25
h = 6
s = w*h
layers = []
for i  in range(0, len(data), s):
    layers.append(data[i:i+s])

composite = [ [] for _ in range(s) ]

for l in reversed(layers):
    for i in range(len(l)):
        composite[i].append(l[i])

for st in composite:
    while st[-1] == '2':
        st.pop()

final = []
for st in composite:
    final.append(st[-1])

for y in range(h):
    line = ''.join(final[y*w:y*w +w]).replace('0', ' ').replace('1', 'X')
    print(line)