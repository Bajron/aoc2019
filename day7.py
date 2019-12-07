#!/usr/bin/env python3

#!/bin/bash
import sys
import queue
import itertools
import threading

input = sys.stdin.read()
program = [int(x) for x in input.split(',')]

class Processor():
    def __init__(self, program, input_queue, output_queue):
        self.program = program.copy()
        self.ip = 0
        self.input_queue = input_queue
        self.output_queue = output_queue

    def get_input(self):
        ret = self.input_queue.get()
        print ('INPUT:', ret)
        return ret

    def put_output(self, v):
        print ('OUTPUT:', v)
        self.output_queue.put(v)

    def get_params(self, count, last_is_immediate=False):
        def get_mode(o, k):
            o = o[-3::-1]
            if k < len(o):
                return int(o[k])
            return 0

        values = [-1] * count

        ip = self.ip
        opcode = str(self.program[ip])
        
        if last_is_immediate:
            count -= 1

        for i in range(0, count):
            p = self.program[self.ip + i + 1]
            if get_mode(opcode, i) == 0:
                p = self.program[p]
            values[i] = p

        if last_is_immediate:
            p = self.program[self.ip + count + 1]
            values[-1] = p
        
        return tuple(values)

    def run(self):
        while self.ip < len(self.program):
            print('IP:', self.ip)
            op = self.program[self.ip] % 100

            if op == 99:
                print('HALT')
                self.ip += 1
                break
            if op == 1:
                p1, p2, p3 = self.get_params(3, last_is_immediate=True)
                self.program[p3] = p1 + p2
                self.ip += 4
            elif op == 2:
                p1, p2, p3 = self.get_params(3, last_is_immediate=True)
                self.program[p3] = p1 * p2
                self.ip += 4
            elif op == 3:
                p1, = self.get_params(1, last_is_immediate=True)
                self.program[p1] = self.get_input()
                self.ip += 2
            elif op == 4:
                p1, = self.get_params(1)
                self.put_output(p1)
                self.ip += 2
            elif op == 5:
                p1, p2 = self.get_params(2)
                self.ip += 3
                if p1 != 0:
                    self.ip = p2
            elif op == 6:
                p1, p2 = self.get_params(2)
                self.ip += 3
                if p1 == 0:
                    self.ip = p2
            elif op == 7:
                p1, p2, p3 = self.get_params(3, last_is_immediate=True)
                self.program[p3] = 1 if p1 < p2 else 0
                self.ip += 4
            elif op == 8:
                p1, p2, p3 = self.get_params(3, last_is_immediate=True)
                self.program[p3] = 1 if p1 == p2 else 0
                self.ip += 4
            else:
                print('invalid opcode', self.program[self.ip])


print(program)


def test():
    processor = Processor(program, queue.Queue(), queue.Queue())
    processor.input_queue.put(5)
    processor.run()
    while not processor.output_queue.empty():
        print ('Ouput:', processor.output_queue.get())


r = range(5)
processors = [None for _ in r]
max_output = -1
max_permutation = None

for permutation in itertools.permutations(r):
    inputs = [queue.Queue() for _ in r]
    output = queue.Queue()
    for i in r:
        processors[i] = Processor(program, inputs[i], inputs[i+1] if i != r[-1] else output)
        inputs[i].put(permutation[i])

    inputs[0].put(0)

    print ('Starting', list(permutation))
    threads = [threading.Thread(target=processors[i].run) for i in r]
    for i in r:
        threads[i].start()
    
    print ('Waiting for output')
    o = output.get()
    if o > max_output:
        max_output = o
        max_permutation = permutation

    print ('Waiting for join')
    for i in r:
        threads[i].join()

print('Max output', max_output, 'for', list(max_permutation))
