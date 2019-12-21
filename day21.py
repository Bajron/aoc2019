#!/usr/bin/env python3

import sys
import queue
import itertools
import threading


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
        self.program.extend([0]*200*1024)
        self.ip = 0
        self.relative = 0
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.running = False
        self.input_provider = None
        self.output_handler = None

    def get_input(self):
        # print (self.id, 'GET INPUT', self.input_queue.qsize())
        if self.input_provider:
            ret = self.input_provider()
        else:
            ret = self.input_queue.get()
        # print (self.id, 'INPUT:', ret)
        return ret

    def put_output(self, v):
        # print (self.id, 'OUTPUT:', v)
        if self.output_handler:
            self.output_handler(v)
        else:
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
                p = self.program[self.ip + count + 1]
            elif m == 2:
                p = self.program[self.ip + count + 1] + self.relative
            values[-1] = Setter(self.program, p)
        
        return tuple(values)

    def run(self):
        self.running = True
        while self.ip < len(self.program):
            #print(self.id, 'IP:', self.ip)
            op = self.program[self.ip] % 100

            if op == 99:
                print(self.id, 'HALT')
                sys.stdout.flush()
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
        self.running = False


def putLine(q, line):
    for i in [ord(ch) for ch in line]:
        q.put(i)
    q.put(10)
    print('Line entered', line)
    sys.stdout.flush()

def readLine(q):
    print('Reading line')
    data = []
    while True:
        ch = q.get(timeout=4)
        if ch == 10: break
        data.append(ch)
    print(''.join(chr(x) for x in data))

inputString = sys.stdin.read()
inputProgram = [int(x) for x in inputString.split(',')]

inQ = queue.Queue()
outQ = queue.Queue()
vm = Processor(0, inputProgram, inQ, outQ)
tvm = threading.Thread(target=vm.run)
tvm.start()

script = [
    'NOT C J',
    'AND D J',
    'NOT A T',
    'OR T J',
    'WALK',
]
    
# @##.#..#
# @...####
# @##.#.####
# @.######
readLine(outQ)

print('Providing input')
for l in script:
    putLine(inQ, l)
sys.stdout.flush()

tvm.join(timeout=3)

if outQ.qsize() == 1:
    print('Single output')
    print('Damage', outQ.get())
else:
    print('Multiple outputs')
    data = []
    try:
        while not outQ.empty():
            ch = outQ.get(timeout=2)
            if ch > 256:
                print('Big output', ch)
            else:
                data.append(ch)
    except queue.Empty:
        pass

    s = ''.join(chr(x) for x in data)
    print(s)
    sys.stdout.flush()
