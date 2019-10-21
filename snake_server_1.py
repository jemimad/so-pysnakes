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

class snake(object):
    def __init__(self, color, pos):
        self.body = []
        self.turns = {}
        self.color = color
        self.head = square(pos, color=self.color)
        self.body.append(self.head)
        self.addSquare()
        self.addSquare()
        self.dirnx = 0
        self.dirny = 1

    def addSquare(self):
        tail = self.body[-1]
        dx, dy = tail.direction[0], tail.direction[1]

        if dx == 1 and dy == 0:
            self.body.append(square((tail.position[0]-1,tail.position[1]), color=self.color))
        elif dx == -1 and dy == 0:
            self.body.append(square((tail.position[0]+1,tail.position[1]), color=self.color))
        elif dx == 0 and dy == 1:
            self.body.append(square((tail.position[0],tail.position[1]-1), color=self.color))
        elif dx == 0 and dy == -1:
            self.body.append(square((tail.position[0],tail.position[1]+1), color=self.color))

        self.body[-1].direction = (dx, dy)

    def move(self):
        global rows
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.position[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.position[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.position[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.position[:]] = [self.dirnx, self.dirny]
        """
        for i, c in enumerate(self.body):
            p = c.position[:]
            if p in self.turns:
                turn = self.turns[p]
                c.position = (c.position[0] + turn[0], c.position[1] + turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.direction[0] == -1 and c.position[0] <= 0: c.position = (rows-1, c.position[1])
                elif c.direction[0] == 1 and c.position[0] >= rows-1: c.position = (0,c.position[1])
                elif c.direction[1] == 1 and c.position[1] >= rows-1: c.position = (c.position[0], 0)
                elif c.direction[1] == -1 and c.position[1] <= 0: c.position = (c.position[0],rows-1)
                else: c.position = (c.position[0] + c.direction[0], c.position[1] + c.direction[1])

    def reset(self, pos):
        global snacks
        self.addSquare()
        corpse = self.body

        self.head = square(pos)
        self.body = []
        self.body.append(self.head)
        self.addSquare()
        self.addSquare()
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

        print("Corpse size:", len(corpse))

        for c in corpse:
            print("Adding snack to", c.position)
            snacks.append(square(c.position, color=(0,255,0)))

    def get_body(self):
        global SNAKE_COLORS

        body_array = []

        for piece in self.body:
            body_array.append(square(piece.position, color=piece.color))

        return body_array

def randomSnack(rows):    
    x = random.randrange(rows)
    y = random.randrange(rows)
        
    return (x,y)

def spawnSnake(list, color, number):
    list.append(snake(color, (10+number,10+number)))  

class square(object):
    def __init__(self, position, color=(0,0,0), direction=(1,0)):
        self.position = position
        self.color = color
        self.direction = direction

class snapshot(object):
    def __init__(self, snakes, snacks):
        self.snakes = []
        self.snacks = snacks

        for snk in snakes:
            self.snakes.append(snk.get_body())

def main ():
    global SNAKE_COLORS, rows

    PORT = 65433
    SNACK_COLOR = (0, 255, 0)
    SNAKE_COLORS = [(255, 0, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]

    rows = 20
    snacks = []
    snakes = []

    max_players = 4
    player_count = 0

    snap = snapshot(snakes, snacks)  
    
    inputs = []
    outputs = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setblocking(0)
        server.bind(('', PORT))
        server.listen(5)
        inputs.append(server)
        clock = pygame.time.Clock()

        while True :
            pygame.time.delay(500)
            clock.tick(10)
            snacks.append(square(randomSnack(rows), SNACK_COLOR))   

            for snk in snakes:
                snk.move()

            readable, writeable, error = select.select(inputs,outputs,[])            
            for sock in readable:
                if sock is server:
                    # WHAT HAPPENS WHEN NEW CLIENT CONNECTS
                    conn, info = sock.accept()
                    inputs.append(conn)
                    print("Connection received from ", info)

                    if player_count < max_players:
                        spawnSnake(snakes, SNAKE_COLORS[player_count], player_count)                        
                        player_count+=1
                    else:
                        sock.close()
                        inputs.remove(sock)
                else:
                    data = sock.recv(1024)
                    if data:
                        # RECEIVE DATA FROM CLIENT
                        print("Received", repr(data))
                        if sock not in outputs:
                            outputs.append(sock)                        
                    else:
                        if sock in outputs:
                            outputs.remove(sock)

                        inputs.remove(sock)
                        sock.close()

            for s in writeable:
                # SEND DATA TO CLIENT
                snap = snapshot(snakes, snacks)  
                data_string = pickle.dumps(snap)
                s.send(data_string)

main()


"""
def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
        
    return (x,y)
"""

"""
    flag = True
    clock = pygame.time.Clock()

    spawnSnack = False
    snackTime = 0
    
    # Game loop
    while flag:
        # Fix FPS
        pygame.time.delay(50)
        clock.tick(10)

        for s in snakes:
            # Snakes moves
            s.move()

            # If snake eats a snack
            if s.body[0].pos in list(map(lambda z:z.pos,snacks)):
                snackTime = pygame.time.get_ticks()

                s.addSquare()
                for sn in snacks:
                    if (sn.pos == s.body[0].pos):
                        snacks.remove(sn)

        if len(snacks) == 0:
            spawnSnack = True

        # If it has to spawn a snack
        if spawnSnack:
            if pygame.time.get_ticks() - snackTime >= 500:
                snacks.append(cube(randomSnack(rows, snakes[0]), color=(0,255,0)))
                spawnSnack = False

        for x in range(len(snakes[0].body)):
            if snakes[0].body[x].pos in list(map(lambda z:z.pos,snakes[0].body[x+1:])):
                print('Score: ', len(snakes[0].body))
                message_box('You Lost!', 'Play again...')
                snakes[0].reset((10,10))                
                break
        
        for y in range(len(snakes)):
            print("y =", y)
            for x in range(len(snakes[y].body)):
                print("x =", x)
                for w in range(y+1, len(snakes)):
                    print("w =", w)
                    print(snakes[y].body[x].pos, "=", list(map(lambda z:z.pos,snakes[w].body[0:])))

                    if snakes[y].body[x].pos in list(map(lambda z:z.pos,snakes[w].body)):
                        print('Score: ', len(snakes[y].body) - 3)
                        message_box('You Lost!', 'Play again...')
                        snakes[y].reset((10,10))
                        break
            
        redrawWindow(win)      
        flag = True  
    pass

    """