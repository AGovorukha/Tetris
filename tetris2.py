#!/usr/bin/python

import pygame, math, random
from pygame import *
from math import *


WIN_WIDTH = 400
WIN_HEIGHT = 400
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BG_COLOR = "#000022"



#PyGame init
pygame.init()
screen = pygame.display.set_mode(DISPLAY)
pygame.display.set_caption("Tetris v0.1")

#Background init
bg = Surface((WIN_WIDTH,WIN_HEIGHT))
bg.fill(Color(BG_COLOR))

#Timer init
timer = pygame.time.Clock()

class base_figure(object):

   def __init__(self, color, width=15, x=200, y=1):
      self.color = color
      self.width = width
      self.height = self.width
      self.x = x
      self.y = y
      
      self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

   def f_draw(self, scrn):
      self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
      pygame.draw.rect(scrn, self.color, self.rect)

class game_figure(object):

   def __init__(self, color, orient, speed=1, x=170, y=2, coord=[[1,0,0,0],[1,0,0,0,],[1,0,0,0],[1,1,1,0]]):
      self.color = color
      self.orient = orient
      self.speed = speed
      self.coord = coord
      self.start_x = x
      self.start_y = y
      self.base = []
      self.collision = False

   def locate_me(self):
      self.base = []
      for line_y in range(len(self.coord)):
         self.y = self.start_y + (16*line_y)
         for line_x in range(len(self.coord[line_y])):
            if self.coord[line_y][line_x] == 0:
               continue
            else:
               self.x = self.start_x + (16*line_x)
               self.base.append(base_figure(self.color, 15, self.x, self.y))
               
   def draw_me(self, scrn):
      for i in range(len(self.base)):
         self.base[i].f_draw(scrn)

   def move(self):
      if self.collision:
         self.speed = 0
      else:
         for i  in range(len(self.base)):
            self.base[i].y = self.base[i].y + self.speed         
      self.start_y = self.base[0].y

   def check_collision(self, other):
      for b in self.base:
         for o in other.base:
            if b.rect.colliderect(pygame.Rect(o.x, o.y - 2, o.width, o.height)):
               self.collision = True
 
   def rotate_me(self):
      m = self.coord
      layers = len(m) / 2
      length = len(m) - 1

      for layer in range(layers): #for each layer
         for i in range(layer, length - layer): # loop through the elements we need to change at each layer
            temp = m[layer][i] #save the top element, it takes just one variable as extra memory
            #Left -> Top
            m[layer][i] = m[length - i][layer]
            #Bottom -> left
            m[length - i][layer] = m[length - layer][length - i]
            #Right -> bottom
            m[length - layer][length - i] = m[i][length - layer]
            #Top -> Right
            m[i][length - layer] = temp
            self.coord = m      
 
class borders(object):
   def __init__(self, x1, x2, y1, y2):
      self.x1 = x1
      self.x2 = x2
      self.y1 = y1
      self.y2 = y2

   def check(self, g_f):
      for i in range(len(g_f.base)):
         if g_f.base[i].y >= self.y2 - g_f.base[i].width:
            g_f.speed = 0
         elif g_f.base[i].y >= self.y2 - (g_f.base[i].width + 6):
            g_f.speed = 1
                
class my_game(object):

   def __init__(self):
      self.points = 0
      self.figures = []
      self.gamer_name = 'Andrii'
      self.flag = True

   def new_figure(self):
         
         self.figures.append(game_figure((0,0,212), 'left', 1, 1, 2, [[1,1,1,1],[0,1,1,0,],[0,1,1,0],[0,0,0,0]]))
         self.figures[-1].locate_me()

   def game_stop(self):
      pass

brd = borders(1, 399, 1, 399)
new_game = my_game()
new_game.new_figure()
gf = new_game.figures[-1]
#gf = game_figure((0,0,212), 'left', 1, 70, 50 )
#gf.locate_me()

#gf2 = game_figure((0,200,0), 'left', 1, 1, 2, [[1,1,0,0],[1,1,0,0,],[0,0,0,0],[0,0,0,0]])
#gf2.locate_me()

#gf = game_figure((0,0,212), 'left', 1, 70, 50, [[0,0,0,0],[0,0,0,0,],[1,1,1,1],[0,0,0,0]])
#gf.locate_me()

done = False
while not done:
   timer.tick(50)
   for e in pygame.event.get():
      if e.type == QUIT:
         done = True
         break

   screen.blit(bg, (0, 0))
#  brd.check(gf2)
   brd.check(gf)
   if len(new_game.figures) >= 2:
      gf.check_collision(new_game.figures[-2])

   if gf.speed != 0:
      gf.move()
   else:
      new_game.new_figure()
      gf = new_game.figures[-1]

   if e.type == KEYDOWN:
      if e.key == K_UP:
         gf.rotate_me()
         gf.locate_me()
         if len(new_game.figures) >= 2:
            gf.check_collision(new_game.figures[-2])
            if gf.collision:
               gf.rotate_me()
               gf.rotate_me()
               gf.rotate_me()
               gf.collision = False
               gf.locate_me()
               e.type = KEYDOWN
   if e.type == KEYDOWN:
      if e.key == K_RIGHT:
         gf.start_x = gf.start_x + 16
         gf.locate_me()

   if e.type == KEYDOWN:
      if e.key == K_LEFT:
         gf.start_x = gf.start_x - 16
         gf.locate_me()


   for F in new_game.figures:
      F.draw_me(screen)
     
   pygame.display.update()


#Farewell
print (":-)")


