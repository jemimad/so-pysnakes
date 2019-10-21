import math
import random
import socket
import pickle
import pygame
import tkinter as tk
from tkinter import messagebox

def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x,0),(x,w))
        pygame.draw.line(surface, (255,255,255), (0,y),(w,y))
         
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
    def __init__(self, position, color=(0,0,0), direction=(1,0)):
        self.position = position
        self.color = color
        self.direction = direction        

def drawSquare(sq, window, isHead=False, width=500, rows=20):
    dis = width // rows
    i = sq.position[0]
    j = sq.position[1]

    pygame.draw.rect(window, sq.color, (i*dis+1,j*dis+1, dis-2, dis-2))

    if isHead:
        centre = dis//2
        radius = 3
        circleMiddle = (i*dis+centre-radius,j*dis+8)
        circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
        pygame.draw.circle(window, (0,0,0), circleMiddle, radius)
        pygame.draw.circle(window, (0,0,0), circleMiddle2, radius)


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

    width = 500
    rows = 20

    window = pygame.display.set_mode((width, width))
    window.fill((0,0,0))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'Hello, world')
        data = s.recv(1024)

    snap = pickle.loads(data)

    for snack in snap.snacks:
        drawSquare(snack, window)

    for snk in snap.snakes:
        for i, piece in enumerate(snk):
            if i ==0:
                drawSquare(piece, window, isHead=True)
            else:
                drawSquare(piece, window)

    for s in snakes:        
        s.draw(window)

    drawGrid(width,rows, window)
    pygame.display.update()

    while True:
        continue



main()