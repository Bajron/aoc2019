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
        print (self.id, 'INPUT:', ret)
        return ret

    def put_output(self, v):
        print (self.id, 'OUTPUT:', v)
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

processor = Processor(0, inputProgram, queue.Queue(), queue.Queue())
processingThread = threading.Thread(target=processor.run)
processingThread.start()

NORTH, SOUTH, WEST, EAST = 1, 2, 3, 4
WALL, MOVED, FOUND = 0, 1, 2

visits = [[0] * 100 for _ in range(100)]
room = [['?'] * 100 for _ in range(100)]
position = 50,50

def nextPos(p,d):
    if d == NORTH: return(p[0] + 1, p[1])
    if d == SOUTH: return(p[0] - 1, p[1])
    if d == EAST: return(p[0], p[1] + 1)
    if d == WEST: return(p[0], p[1] - 1)

def reverseDirection(d):
    if d == NORTH: return SOUTH
    if d == SOUTH: return NORTH
    if d == EAST: return WEST
    if d == WEST: return EAST

def genMoves(position):
    moves = [ (dir, nextPos(position, dir)) for dir in [NORTH, SOUTH, WEST, EAST] ]
    moves = [ (x[0], visits[x[1][0]][x[1][1]]) for x in moves]
    moves.sort(key=lambda x: x[1])

    return [ x[0] for x in moves ]

path = []
path.append([position, 0, 0, genMoves(position)])
room[position[0]][position[1]] = 'O'
found = None

while len(path) > 0:
    print ('Path', len(path), path[-1])
    position = path[-1][0]
    
    y,x = position
    visits[y][x] = visits[y][x] + 1

    i = path[-1][2]
    moves = path[-1][3]

    appended = False
    while i < len(moves):
        m = moves[i]
        i += 1
        np = nextPos(position, m)

        if visits[np[0]][np[1]] > 0:
            print('Not going', np, 'already visited')
            continue

        processor.input_queue.put(m)
        result = processor.output_queue.get()
        
        if result == WALL:
            room[np[0]][np[1]] = '#'
            visits[np[0]][np[1]] = 1000
            continue

        if result == FOUND:
            print('Found', np)
            found = np
            room[np[0]][np[1]] = 'X'
        elif result == MOVED:
            room[np[0]][np[1]] = '.'

        path[-1][2] = i
        path.append([np, m, 0, genMoves(np)])
        appended = True
        break

    if not appended:
        if path[-1][1] == 0:
            print ('Backtrack from origin')
        else:
            print ('Backtrack from', position)
            backDirection = reverseDirection(path[-1][1])
            processor.input_queue.put(backDirection)
            result = processor.output_queue.get()
            if result == FOUND:
                print ('Found on backtrack')
                found = position[-2][0]
        
        path.pop()


for row in room:
    print(''.join(row))

print('Found in',found)

# to close the VM
processor.input_queue.put(0)

bfsVisited = [[-1]*100 for _ in range(100)]
bfs = []
bfs.append(found)

iteration = 0
while bfs:
    l = len(bfs)
    for i in range(l):
        cur = bfs[i]
        y,x = cur
        if bfsVisited[y][x] != -1:
            continue
        
        bfsVisited[y][x] = iteration
        
        if room[y][x] == '#':
            continue

        bfs.extend([nextPos(cur, dir) for dir in [NORTH, SOUTH, WEST, EAST]])
    iteration += 1
    bfs = bfs[l:]


maxIterationForRoom = 0
for y in range(len(room)):
    for x in range(len(room[y])):
        if room[y][x] != '#' and room[y][x] != '?':
            v = bfsVisited[y][x]
            if v > maxIterationForRoom:
                maxIterationForRoom = v

print('Last oxygen at', maxIterationForRoom)