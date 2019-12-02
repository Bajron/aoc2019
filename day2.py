#!/bin/bash
import sys

input = sys.stdin.read()
program = [int(t) for t in input.split(',')]
print(program)
print('Setting 12 02')
program[1] = 12
program[2] = 2
print(program)
p = 0
while p < len(program) and program[p] != 99:
    print('Iteration', p)
    opcode = program[p]
    if opcode == 1:
        program[program[p+3]] = program[program[p+1]] + program[program[p+2]]
    elif opcode == 2:
        program[program[p+3]] = program[program[p+1]] * program[program[p+2]]
    else:
        print('invalid opcode', opcode)
    p += 4

print(program)
print(program[0])