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
        self.program.extend([0]*1024)
        self.ip = 0
        self.relative = 0
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.running = False
        self.input_provider = None
        self.output_handler = None

    def get_input(self):
        #print (self.id, 'GET INPUT', self.input_queue.qsize())
        if self.input_provider:
            ret = self.input_provider()
        else:
            ret = self.input_queue.get()
        #print (self.id, 'INPUT:', ret)
        return ret

    def put_output(self, v):
        #print (self.id, 'OUTPUT:', v)
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
                #print(self.id, 'HALT')
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



inputString = sys.stdin.read()
inputProgram = [int(x) for x in inputString.split(',')]

inQ = queue.Queue()
outQ = queue.Queue()

def getPoint(x,y):
    vm = Processor(0, inputProgram, inQ, outQ)
    inQ.put(x)
    inQ.put(y)
    vm.run()
    return outQ.get()

def getFirstLastX(y):
    x = 0
    while getPoint(x, y) != 1:
        x += 1
    firstX = x

    while getPoint(x, y)  != 0:
        x += 1
    lastX = x

    return firstX, lastX

def getLine(y, len):
    line = []
    for x in range(len):
        vm = Processor(0, inputProgram, inQ, outQ)
        inQ.put(x)
        inQ.put(y)
        vm.run()
        result = outQ.get()
        line.append(result)
    return line

def getLine2(y, X, top):
    line = []
    for x in range(X, top):
        vm = Processor(0, inputProgram, inQ, outQ)
        inQ.put(x)
        inQ.put(y)
        vm.run()
        result = outQ.get()
        line.append(result)
    return line

y = 10
line = []
while sum(line) < 100:
    y *= 2
    print('Checking', y)
    line = getLine(y, y + y//2)
        
print('y', y, ' has ', sum(line))
for x in range(y):
    if line[x] == 1:
        break
print('x',x)

while True:
    print ('Checking ', y)
    firstX, lastX = getFirstLastX(y)
    yEnd = y + 99
    fx, lx = getFirstLastX(yEnd)

    bottomRight = getPoint(lastX, yEnd)
    if bottomRight != 1:
        y += fx - firstX + 1
        continue
    bottomLeft = getPoint(lastX - 99, yEnd)
    if bottomLeft != 1:
        y += fx - lastX + 99 +1
        continue

    break

print ('Got something', y)
print ('X ranges are', getFirstLastX(y))


while True:
    print ('Refining ', y)
    prevY = y - 1
    firstX, lastX = getFirstLastX(prevY)
    yEnd = prevY + 99
    fx, lx = getFirstLastX(yEnd)


    bottomRight = getPoint(lastX, yEnd)
    bottomLeft = getPoint(lastX - 99, yEnd)

    if bottomLeft == 1 and bottomRight == 1:
        y = prevY
        continue

    break

# not 843 1088
# not 836 1079 too low
print ('Refined to y', y)
refinedY = y
firstX, lastX = getFirstLastX(y)
print ('X ranges top', firstX, lastX)
print ('X ranges bottom', getFirstLastX(y+99))

print ('X should be ', lastX - 99)
print ('Result code', 10000*(lastX - 99) + y)

print('Starting at y', refinedY-10)
print('x starts at', 800)
for y in range(refinedY - 10, refinedY + 110):
    line = getLine2(y, 800, 1100)
    print(''.join(str(x) for x in line))

