import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class cube(object):
    rows = 20
    def __init__(self, start, dirnx = 1, dirny = 0, color = [0, 0, 0]):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes = False):
        dist = size // rows
        rw = self.pos[0]
        cm = self.pos[1]
        pygame.draw.rect(surface, self.color, (rw * dist + 1, cm * dist + 1, dist - 2, dist - 2))

        if eyes:
            center = dist // 2
            radius = 3
            circle_middle = (rw * dist + center - radius * 2, cm * dist + 8)
            circle_middle2 = (rw * dist + center + radius * 2, cm * dist + 8)
            pygame.draw.circle(surface, (255,255,255), circle_middle, radius)
            pygame.draw.circle(surface, (255,255,255), circle_middle2, radius)
 

class snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.addcube()
        self.addcube()
        self.dirnx = 0
        self.dirny = 1


    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            #move in 4 directions
            if keys[pygame.K_LEFT]:
                self.dirx = -1
                self.diry = 0
                self.turns[self.head.pos[:]] = [self.dirx, self.diry]
            elif keys[pygame.K_RIGHT]:
                self.dirx = 1
                self.diry = 0
                self.turns[self.head.pos[:]] = [self.dirx, self.diry]
            elif keys[pygame.K_UP]:
                self.dirx = 0
                self.diry = -1
                self.turns[self.head.pos[:]] = [self.dirx, self.diry]
            elif keys[pygame.K_DOWN]:
                self.dirx = 0
                self.diry = 1
                self.turns[self.head.pos[:]] = [self.dirx, self.diry]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn  = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)

            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)



    def reset(self, pos):
        i = 0
        for cube in s.body[1:]:
            if pos == cube.pos:
                s.body = s.body[:i]
                break
            i = i + 1



    def addcube(self):
        tail = self.body[-1]
        dx = tail.dirnx
        dy = tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

def draw_grid(w, rows, surface):
    size_between = w // rows
    x = 0
    y = 0
    for i in range(rows):
        x = x + size_between
        y = y + size_between
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))     

def draw_window(surface):
    surface.fill((135,206,250)) #RGB
    s.draw(surface)
    apple.draw(surface)
    draw_grid(size, rows, surface)
    pygame.display.update()

def rand_apple(snake):
    position = snake.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x,y), position))) > 0:
            continue
        else:
            break
    return (x, y)


def main():
    global size, rows, s, apple
    size = 700 #wielkosc okna
    rows = 20

    window = pygame.display.set_mode((size, size))

    s = snake((0, 0, 0), (10, 10))
    apple = cube(rand_apple(s), color = [255, 0 , 0])
    run = True
    clock = pygame.time.Clock()
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    print(s.body[1].pos)
   

    while run:

        pygame.time.delay(50) #mniej gra szybsza
        clock.tick(10)          #mniej gra wolniejsza
        s.move()
        s.reset(s.body[0].pos)
        '''if s.body[0] in s.body[1:]:
            pygame.quit()'''

        #check if eat apple
        if s.body[0].pos == apple.pos:
            s.addcube()
            apple = cube(rand_apple(s), color = [255, 0 , 0])

        draw_window(window)
         

main()
