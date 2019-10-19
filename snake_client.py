import math
import random
import socket
import pickle
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
    def __init__(self, body):
        self.body = []

        for piece in body:
            self.body.append(cube(piece.position, color=piece.color))
            
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i ==0:
                c.draw(surface, True)
            else:
                c.draw(surface)

def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x,0),(x,w))
        pygame.draw.line(surface, (255,255,255), (0,y),(w,y))
      
def redrawWindow(surface):
    global rows, width, snakes, snacks
    surface.fill((0,0,0))

    for s in snakes:        
        s.draw(surface)

    for s in snacks:
        s.draw(surface)

    drawGrid(width,rows, surface)
    pygame.display.update()

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

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

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

def main():
    global width, rows, snakes, snacks

    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 65433        # The port used by the server

    snacks = []
    snakes = []  

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'Hello, world')
        data = s.recv(1024)

    snap = pickle.loads(data)

    for snack in snap.snacks:
        snacks.append(cube(snack.position, color=snack.color))

    for snk in snap.snakes:
        snakes.append(snake(snk))    

    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    
    redrawWindow(win)

    while True:
        continue

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

                s.addCube()
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

main()