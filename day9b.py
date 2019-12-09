#!/usr/bin/env python3

#!/bin/bash
import sys
import queue
import itertools
import threading

input = sys.stdin.read()
program = [int(x) for x in input.split(',')]

class Setter():
    def __init__(self, program, index):
        self.program = program
        self.index = index

    def set(self, value):
        self.program[self.index] = value


class Processor():
    def __init__(self, id, program, input_queue, output_queue):
        self.id = id
        self.program = program.copy()
        self.program.extend([0]*1024*1024)
        self.ip = 0
        self.relative = 0
        self.input_queue = input_queue
        self.output_queue = output_queue

    def get_input(self):
        ret = self.input_queue.get()
        print (self.id, 'INPUT:', ret)
        return ret

    def put_output(self, v):
        print (self.id, 'OUTPUT:', v)
        self.output_queue.put(v)

    def get_params(self, count, last_is_to_set=False):
        def get_mode(o, k):
            o = o[-3::-1]
            if k < len(o):
                return int(o[k])
            return 0

        values = [-1] * count

        ip = self.ip
        opcode = str(self.program[ip])
        
        if last_is_to_set:
            count -= 1

        for i in range(0, count):
            m = get_mode(opcode, i)
            index = self.ip + i + 1
            p = self.program[index]
            if m == 0:
                p = self.program[p]
            elif m == 2:
                p = self.program[p + self.relative]

            values[i] = p

        if last_is_to_set:
            m = get_mode(opcode, count)
            if m == 0:
                p = program[self.ip + count + 1]
            elif m == 2:
                p = program[self.ip + count + 1] + self.relative
            values[-1] = Setter(self.program, p)
        
        return tuple(values)

    def run(self):
        while self.ip < len(self.program):
            print(self.id, 'IP:', self.ip)
            op = self.program[self.ip] % 100

            if op == 99:
                print(self.id, 'HALT')
                self.ip += 1
                break
            if op == 1:
                p1, p2, p3 = self.get_params(3, last_is_to_set=True)
                p3.set(p1 + p2)
                self.ip += 4
            elif op == 2:
                p1, p2, p3 = self.get_params(3, last_is_to_set=True)
                p3.set(p1 * p2)
                self.ip += 4
            elif op == 3:
                p1, = self.get_params(1, last_is_to_set=True)
                p1.set(self.get_input())
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
                p1, p2, p3 = self.get_params(3, last_is_to_set=True)
                p3.set(1 if p1 < p2 else 0)
                self.ip += 4
            elif op == 8:
                p1, p2, p3 = self.get_params(3, last_is_to_set=True)
                p3.set(1 if p1 == p2 else 0)
                self.ip += 4
            elif op == 9:
                p1, = self.get_params(1)
                self.relative += p1
                self.ip += 2
            else:
                print(self.id, 'invalid opcode', self.program[self.ip])


print(program)


processor = Processor(0, program, queue.Queue(), queue.Queue())
processor.input_queue.put(2)
processor.run()
while not processor.output_queue.empty():
    print ('Ouput:', processor.output_queue.get())

