#!/bin/bash
import sys

input = sys.stdin.read()
program = [int(x) for x in input.split(',')]
print(program)

input_queue = [5]
output_queue = []

def get_input():
    global input_queue
    ret = input_queue[-1]
    print ('INPUT:', ret)
    input_queue = input_queue[:-1]
    return ret

def put_output(v):
    global output_queue
    print ('OUTPUT:', v)
    output_queue.append(v)

def get_mode(o, k):
    o = o[-3::-1]
    if k < len(o):
        return int(o[k])
    return 0

ip = 0
while ip < len(program):
    print('IP:', ip)

    opcode = str(program[ip])
    op = int(opcode[-2:], base=10)

    if op == 99:
        print('HALT')
        ip += 1
        break
    if op == 1:
        p1 = program[ip + 1]
        if get_mode(opcode, 0) == 0: p1 = program[p1]
        p2 = program[ip + 2]
        if get_mode(opcode, 1) == 0: p2 = program[p2]

        p3 = program[ip + 3]

        program[p3] = p1 + p2
        
        ip += 4
    elif op == 2:
        p1 = program[ip + 1]
        if get_mode(opcode, 0) == 0: p1 = program[p1]
        p2 = program[ip + 2]
        if get_mode(opcode, 1) == 0: p2 = program[p2]

        p3 = program[ip + 3]

        program[p3] = p1 * p2
        
        ip += 4
    elif op == 3:
        p1 = program[ip + 1]
        
        program[p1] = get_input()
        
        ip += 2
    elif op == 4:
        p1 = program[ip + 1]
        if get_mode(opcode, 0) == 0: p1 = program[p1]

        put_output(p1)
        
        ip += 2
    elif op == 5:
        p1 = program[ip + 1]
        if get_mode(opcode, 0) == 0: p1 = program[p1]
        p2 = program[ip + 2]
        if get_mode(opcode, 1) == 0: p2 = program[p2]

        ip += 3
        if p1 != 0:
            ip = p2
    elif op == 6:
        p1 = program[ip + 1]
        if get_mode(opcode, 0) == 0: p1 = program[p1]
        p2 = program[ip + 2]
        if get_mode(opcode, 1) == 0: p2 = program[p2]

        ip += 3
        if p1 == 0:
            ip = p2
    elif op == 7:
        p1 = program[ip + 1]
        if get_mode(opcode, 0) == 0: p1 = program[p1]
        p2 = program[ip + 2]
        if get_mode(opcode, 1) == 0: p2 = program[p2]

        p3 = program[ip + 3]

        program[p3] = 1 if p1 < p2 else 0
        
        ip += 4
    elif op == 8:
        p1 = program[ip + 1]
        if get_mode(opcode, 0) == 0: p1 = program[p1]
        p2 = program[ip + 2]
        if get_mode(opcode, 1) == 0: p2 = program[p2]

        p3 = program[ip + 3]

        program[p3] = 1 if p1 == p2 else 0
        
        ip += 4
    else:
        print('invalid opcode', opcode)


print(program)
print(program[0])

print('Output:',*output_queue)