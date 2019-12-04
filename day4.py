#!/usr/bin/env python3

input = range(130254, 678275 + 1, 1)

counter = 0

def hasDouble(s):
    c = s[0]
    for i in range(1,len(s)):
        if s[i] == c:
            return True
        c = s[i]
    return False

def isIncreasing(s):
    c = s[0]
    for i in range(1,len(s)):
        if s[i] < c:
            return False
        c = s[i]
    return True

for i in input:
    s = str(i)
    if isIncreasing(s) and hasDouble(s):
        counter += 1


print(counter)