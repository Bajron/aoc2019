#!/usr/bin/env python3

import sys
import queue
import itertools
import threading
import time


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

def putLineInteractive(q):
    line = input('> ')
    line = line.strip()

    global pos
    if line == 'north':
        pos = (pos[0]-1, pos[1])
    elif line == 'south':
        pos = (pos[0]+1, pos[1])
    elif line == 'west':
        pos = (pos[0], pos[1]-1)
    elif line == 'east':
        pos = (pos[0], pos[1]+1)
    elif line == 'map':
        global room
        for r in room:
            print(''.join(r))
        return
    elif line.startswith('hack '):
        global vm
        direction = line.split(' ')[1]

        inventory = []
        putLine(q, 'inv')
        invData = readLines(vm.output_queue)
        for l in invData.split('\n'):
            if l.startswith('- '):
                inventory.append(l.strip(' \n\t-'))

        print('Hacking with', inventory)

        for s in itertools.product([0,1], repeat=len(inventory)):
            print('Hacking combination', s)
            for i in range(len(s)):
                if s[i] == 0:
                    putLine(q, 'drop ' + inventory[i])
            readLines(vm.output_queue)

            putLine(q, direction)
            info = readLines(vm.output_queue)
            if 'ejected' not in info:
                break

            for i in range(len(s)):
                if s[i] == 0:
                    putLine(q, 'take ' + inventory[i])
            readLines(vm.output_queue)
        return
        
    for i in [ord(ch) for ch in line]:
        q.put(i)
    q.put(10)
    print('Line entered "{}"'.format(line))
    sys.stdout.flush()

def readLines(q):
    # print('Reading line')
    data = []
    try:
        while True:
            ch = q.get(timeout=0.1)
            # if ch == 10: break
            data.append(ch)
    except queue.Empty:
        if not data:
            print('No output')
    ret = ''.join(chr(x) for x in data)
    print(ret)
    sys.stdout.flush()
    return ret

inputString = open(sys.argv[1]).read()
inputProgram = [int(x) for x in inputString.split(',')]

vm = Processor(0, inputProgram, queue.Queue(), queue.Queue())
t = threading.Thread(target=vm.run)
t.start()


room = [['?'] * 60 for _ in range(60)]
pos = (30,30)

forbidden = ['molten lava', 'infinite loop', 'escape pod', 'photons', 'giant electromagnet']

while True:
    room[pos[0]][pos[1]] = '.'
    r = readLines(vm.output_queue)
    
    # Autotake
    entered = r.split('Doors here lead:')
    if len(entered) > 1:
        rest = r.split('Doors here lead:')[1]
        data = rest.split('Items here:')
        
        if len(data) > 1:
            items = data[1].replace('Command?', '')
            for l in items.split('-'):
                l = l.strip('\n\r \t' + chr(10))
                if l and l not in forbidden:
                    putLine(vm.input_queue, 'take ' + l)
                    readLines(vm.output_queue)

    
    # directions = data[0]
    # for l in directions.split('-'):
    #     l = l.strip()
    #     if l:
            
    putLineInteractive(vm.input_queue)




# You drop the easter egg.
# You drop the fuel cell.
# You drop the hologram.
# You drop the manifold.
