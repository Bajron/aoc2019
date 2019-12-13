#!/usr/bin/env python3

import sys
import queue
import itertools
import threading

inputString = sys.stdin.read()
program = [int(x) for x in inputString.split(',')]

class Setter():
    def __init__(self, program, index):
        self.program = program
        self.index = index

    def set(self, value):
        # if self.index == 387:
        #     print('!!!! 387 setting', value)
        #     if value == 0:
        #         value = 1
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
        print (self.id, 'GET INPUT', self.input_queue.qsize())
        if self.input_provider:
            ret = self.input_provider()
        else:
            ret = self.input_queue.get()
        print (self.id, 'INPUT:', ret)
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


def signum(n):
    if n == 0: return 0
    if n < 0: return -1
    return 1

def toChar(i):
    if i <= 0: return ' '
    if i == 1: return '#'
    if i == 2: return '%'
    if i == 3: return '='
    if i == 4: return 'O'

print(program)
screen = [[-1] * 40 for _ in range(22)]
program[0] = 2
processor = Processor(0, program, queue.Queue(), queue.Queue())
score = 0

# processor.run()
prevBall = None
ball, paddle = None, None

def moveJoystick():
    global prevBall, ball, paddle
    
    if ball and paddle:
        # if prevBall and ball:
        #     ballDiff = (ball[0] - prevBall[0], ball[1] - prevBall[1])
        #     nextBall = (ball[0] + ballDiff[0], ball[1] + ballDiff[1])
        #     print('Predictive')
        #     return signum(nextBall[1] - paddle[1])
        print('Normal')
        return signum(ball[1] - paddle[1])
    else:
        return 0

reading = 0
x, y, t = None, None, None
def updateScreen(input):
    global reading, score, prevBall, ball, paddle, x, y, screen
    if reading == 0:
        reading += 1
        x = input
        return
    if reading == 1:
        reading += 1
        y = input
        return
    
    reading = 0
    t = input

    if t == 4:
        prevBall = ball
        ball = (y,x)

    if t == 3:
        paddle = (y,x)

    if x == -1 and y == 0:
        score = t
        print('Score',score, ' ball ', ball)
        for row in screen: print(''.join(map(toChar, row)))
    else:
        screen[y][x] = t
    

processor.input_provider = moveJoystick
processor.output_handler = updateScreen

# t = threading.Thread(target=processor.run)
# t.start()

processor.run()
for row in screen: print(''.join(map(toChar, row)))

# while True:
#     processor.run()
#     for row in screen: print(''.join(map(toChar, row)))

#     run = False
#     for row in screen:
#         if 2 in row:
#             run = True
#             break
#     if not run:
#         break
# print ('loop stoped')
# for row in screen: print(''.join(map(toChar, row)))