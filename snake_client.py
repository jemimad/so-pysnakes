import math
import random
import socket
import pickle
import pygame
import sys
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
    PORT = 65435        # The port used by the server

    snacks = []
    snakes = [] 
    

    width = 500
    rows = 20

    window = pygame.display.set_mode((width, width))    

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        my_ip, my_port = s.getsockname()

        while True:
            data = s.recv(15336)

            # RENDER LOGIC COMES HERE
            window.fill((0,0,0))
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

            # INPUT LOGIC COMES HERE
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                keys = pygame.key.get_pressed()
                input_key = (-1, -1)
                
                for key in keys:
                    if keys[pygame.K_LEFT]:
                        input_key = (-1, 0)

                    elif keys[pygame.K_RIGHT]:
                        input_key = (1, 0)

                    elif keys[pygame.K_UP]:
                        input_key = (0, -1)

                    elif keys[pygame.K_DOWN]:
                        input_key = (0, 1)

                if input_key != (-1, -1):
                    input_string = pickle.dumps((input_key, (my_ip, my_port)))
                    s.sendall(input_string)
                
        s.close()

main()