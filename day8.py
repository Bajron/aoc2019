#!/usr/bin/env python3

import sys

data = sys.stdin.read().strip()
print(data)

w = 25
h = 6
s = w*h
layers = []
for i  in range(0, len(data), s):
    #print('getting', i)
    layers.append(data[i:i+s])

print(layers)

def count(layer, digit):
    return sum(map(lambda x: 1 if x == digit else 0, layer))

print(count(layers[0], '0'))

min_zeros = s + 1
min_zeros_layer = -1
for l in layers:
    c = count(l, '0')
    if c < min_zeros:
        min_zeros = c
        min_zeros_layer = l

print(count(min_zeros_layer,'1') * count(min_zeros_layer,'2'))