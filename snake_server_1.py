import math
import random
import socket
import pickle
import select
import time
import sys

import pygame
import tkinter as tk
from tkinter import messagebox

class cube(object):
    rows = 20
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
        
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

class snake(object):
    def __init__(self, color, pos):
        self.body = []
        self.turns = {}
        self.color = color
        self.head = cube(pos, color=self.color)
        self.body.append(self.head)
        self.addCube()
        self.addCube()
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1]), color=self.color))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1]), color=self.color))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1), color=self.color))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1), color=self.color))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy 

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dirnx,c.dirny)        

    def reset(self, pos):
        global snacks
        self.addCube()
        corpse = self.body

        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.addCube()
        self.addCube()
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

        print("Corpse size:", len(corpse))

        for c in corpse:
            print("Adding snack to", c.pos)
            snacks.append(cube(c.pos, color=(0,255,0)))

    def get_body(self):
        global SNAKE_COLORS

        body_array = []

        for piece in self.body:
            body_array.append(square(piece.pos, color=piece.color))

        return body_array

def randomSnack(rows):    
    x = random.randrange(rows)
    y = random.randrange(rows)
        
    return (x,y)

class square(object):
    def __init__(self, position, color=(0,0,0), isHead=False, direction=(0,0)):
        self.position = position
        self.color = color
        self.isHead = isHead
        self.direction = direction

class snapshot(object):
    def __init__(self, snakes, snacks):
        self.snakes = snakes
        self.snacks = snacks

def main ():
    global SNAKE_COLORS
    PORT = 65433
    SNACK_COLOR = (0, 255, 0)
    SNAKE_COLORS = [(255, 0, 0), (0, 0, 255)]

    rows = 20
    snacks = []
    snakes = []

    snakes.append(snake(SNAKE_COLORS[0], (10,10)).get_body())  
    snakes.append(snake(SNAKE_COLORS[1], (11,11)).get_body())  
    snacks.append(square(randomSnack(rows), SNACK_COLOR))   

    snap = snapshot(snakes, snacks)  
    
    read_list = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setblocking(0)
        s.bind(('', PORT))
        s.listen(5)
        read_list.append(s)
        while True :
            readable, writeable, error = select.select(read_list,[],[])
            for sock in readable:
                if sock is s:
                    conn, info = sock.accept()
                    read_list.append(conn)
                    print("Connection received from ", info)
                else:
                    data = sock.recv(1024)
                    if data:
                        print("Received", repr(data))
                        data_string = pickle.dumps(snap)
                        sock.send(data_string)
                    else:
                        sock.close()
                        read_list.remove(sock)

main()