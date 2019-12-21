#!/usr/bin/env python3

import sys
import queue
import itertools
import threading
import copy

def putLine(q, line):
    for i in [ord(ch) for ch in line]:
        q.put(i)
    q.put(10)
    print('Line entered', line)
    sys.stdout.flush()

def readLine(q):
    #print('Reading line')
    data = []
    while True:
        ch = q.get(timeout=4)
        if ch > 255:
            print('\nNon ASCII output', ch, '\n')
            continue
        if ch == 10: break
        data.append(ch)
    print(''.join(chr(x) for x in data))

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
        self.program.extend([0]*10*1024*1024)
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
        self.running = False



inputString = sys.stdin.read()
inputProgram = [int(x) for x in inputString.split(',')]

cpu = Processor(0, inputProgram, queue.Queue(), queue.Queue())
cpu.run()

string = ''
while not cpu.output_queue.empty():
    string += chr(cpu.output_queue.get())

lines = string.split(chr(10))
for l in lines:
    print(l, len(l))

linesFiltered = []
for l in lines:
    if len(l) > 0:
        linesFiltered.append(l)

lines = linesFiltered

#lines = [ l.strip() for l in  sys.stdin.readlines()]

H = len(lines)
W = len(lines[0])

def isScaffolding(ch):
    return ch in '#^<>v'

def isRobot(ch):
    return ch in '^<>v'

NORTH, SOUTH, EAST, WEST = 0,1,2,3

robotDir = None
robotPos = None 
intersections = []
for y in range(H):
    for x in range(W):
        if isScaffolding(lines[y][x]):
            dirs = [0, 0, 0, 0]
            if x > 0 and isScaffolding(lines[y][x-1]):
                dirs[WEST] = 1
            if x < W-1 and isScaffolding(lines[y][x+1]):
                dirs[EAST] = 1
            if y > 0 and isScaffolding(lines[y-1][x]):
                dirs[NORTH] = 1
            if y <H-1 and isScaffolding(lines[y+1][x]):
                dirs[SOUTH] = 1
            
            if sum(dirs) > 2:
                intersections.append((y,x))
        if isRobot(lines[y][x]):
            robotPos = (y,x)
            robotDir = lines[y][x]


def next(pos, dir):
    y,x = pos
    if dir == '^': return (y-1, x)
    if dir == '<': return (y, x-1)
    if dir == '>': return (y, x+1)
    if dir == 'v': return (y+1, x)

def turnLeft(dir):
    if dir == '^': return '<'
    if dir == '<': return 'v'
    if dir == '>': return '^'
    if dir == 'v': return '>'

def turnRight(dir):
    if dir == '^': return '>'
    if dir == '<': return '^'
    if dir == '>': return 'v'
    if dir == 'v': return '<'

def posInBound(pos):
    y,x = pos
    return 0 <= y and y < H and 0 <= x and x < W

visitedIntersection = {}
intersectionSet = set()
for i in intersections:
    visitedIntersection[i] = 0
    intersectionSet.add(i)

print ('Intersections', len(intersections))
#sys.exit(0)

paths = []
def sillyMove(pathIn, dir, pos, count):
    path = pathIn.copy()

    # look around on intersections
    if False and pos in intersectionSet:
        if visitedIntersection[pos] == 2:
            #print('loop, backtrack', path)
            return
        visitedIntersection[pos] = visitedIntersection[pos] + 1
        left = turnLeft(dir)
        sillyMove(path + [str(count), 'L'], left, next(pos, left), 1)

        right = turnRight(dir)
        sillyMove(path + [str(count), 'R'], right, next(pos, right), 1)
         
        visitedIntersection[pos] = visitedIntersection[pos] - 1
    
    forward = next(pos, dir)
    fy, fx = forward
    
    if posInBound(forward) and lines[fy][fx] == '#':
        sillyMove(path, dir, forward, count + 1)
    
    else:
        if count > 0:
            path.append(str(count))
            count = 0
        # can only turn left or righ

        left = turnLeft(dir)
        leftCheck = next(pos, left)
        ly,lx = leftCheck
        if posInBound(leftCheck) and lines[ly][lx] == '#':
            path.append('L')
            return sillyMove(path, left, pos, count)
        
        right = turnRight(dir)
        rightCheck = next(pos, right)
        ry, rx = rightCheck
        if posInBound(rightCheck) and lines[ry][rx] == '#':
            path.append('R')
            return sillyMove(path, right, pos, count)
        
        # or that's the dead end
        paths.append(path)
        print('Found path', path)
        sys.stdout.flush()
        return

sillyMove([], robotDir, robotPos, 0)
print('Found paths:', len(paths))

def findall(haystack, needle):
    finds = []
    i = haystack.find(needle)
    while i >= 0:
        finds.append(i)
        i = haystack.find(needle, i + len(needle))
    return finds

pp = ','.join(paths[0])
ppOriginal = pp
print('Path lenght', len(paths[0]))
print(pp)
funcs = {}

foundSets = []
def recursiveReduce(pp, funcSet, depth=0):
    if depth == 3:
        if len(pp) == 0:
            foundSets.append(copy.copy(funcSet))
        return
    
    comma = pp.index(',')
    comma = pp.index(',', comma + 1)
    commas = 1
    
    while commas < 20:
        funcSet[chr(ord('A') + depth)] = pp[:comma]
        recursiveReduce(pp.replace(pp[:comma], '').strip(','), funcSet, depth+1)
        
        comma = pp.find(',', comma+1)
        if comma < 0:
            break
        commas += 1

recursiveReduce(ppOriginal,{})
print('Found replacement sets', len(foundSets))
print(foundSets)

pp = ppOriginal
funcs = foundSets[0]
for f in ['A', 'B', 'C']:
    print('replacing', f, funcs[f])
    pp = pp.replace(funcs[f], f)
    print(pp)

print('After processing =', pp)

cleaningProgram = inputProgram.copy()
cleaningProgram[0] = 2

inQ = queue.Queue()
outQ = queue.Queue()

vm = Processor(1, cleaningProgram, inQ, outQ)
vmt = threading.Thread(target=vm.run)
vmt.start()

putLine(inQ, pp)
putLine(inQ, funcs['A'])
putLine(inQ, funcs['B'])
putLine(inQ, funcs['C'])
putLine(inQ, 'n')

while vm.running or not outQ.empty():
    readLine(outQ)


