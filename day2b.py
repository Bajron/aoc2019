#!/bin/bash
import sys

input = sys.stdin.read()
program = [int(t) for t in input.split(',')]
print(program)
expect = 19690720

def run(program, noun, verb):
    program[1] = noun
    program[2] = verb
    p = 0
    while p < len(program) and program[p] != 99:
        opcode = program[p]
        if opcode == 1:
            program[program[p+3]] = program[program[p+1]] + program[program[p+2]]
        elif opcode == 2:
            program[program[p+3]] = program[program[p+1]] * program[program[p+2]]
        else:
            print('invalid opcode', opcode)
        p += 4
    return program[0]


for n in range(100):
    for v in range(100):
        result = run(program.copy(), n, v)
        if result == expect:
            print('Match for', n, v)
            print(100 * n + v)

