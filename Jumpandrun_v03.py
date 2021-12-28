import pygame
import numpy as np
import random
import math
import sys
import os
import time

from numpy.core.numeric import True_
from pathlib import Path
from pygame import Rect, constants
from PIL import Image, ImageDraw
from pygame.key import get_pressed
from pygame.key import get_mods

### CONSTANTS ###

PATH = Path("data/")

# Windows #
WIN_HEIGHT = 800
WIN_WIDTH = 1000


surface = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))

# Colors #
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 215, 0)
DARKGREEN = (0, 205, 155)

# Framerate #
FPS = 40
TIME_DELAY = int(1000 / FPS)

# Constants #
sx=0
sy=0
SPEED = np.array([sx, sy])
sx_OP = 2
sy_OP = 0
SPEED_OP = np.array([sx_OP,sy_OP])

friction_coefficent_positive = 0.05
friction_coefficent_negative = -0.05
YSpeed = -20

Grafitation = 1

TEXT_SIZE = 50
size = [WIN_WIDTH, WIN_HEIGHT]
screen = pygame.display.set_mode(size)

### FUNCTIONS ###
def draw_text(text, x, y, color):
    font = pygame.font.SysFont("arial", TEXT_SIZE)
    y_pos = y
    x_pos = x
    text = font.render(text, 1, color)
    screen.blit(text, (x_pos, y_pos))
    pygame.display.update()

## Classes ##
class Object(pygame.sprite.Sprite):
    def __init__(self, img_path, xy_center, v, mass):
        # ASSIGN CLASS ATTRIBUTES
        super().__init__()  # call __init__ of parent class 
        if not os.path.exists(img_path):
            raise Exception(
                "THE FOLLOWING FILE DOES NOT EXIST: {0}".format(img_path))
        self.image = pygame.image.load(str(img_path))  # load image
        self.rect = self.image.get_rect()  # create rectangle containing ball image
        self.rect.center = (int(xy_center[0]), int(xy_center[1]))  # set center coords of ball
        self.mask = pygame.mask.from_surface(self.image)# creates a mask, used for collision detection (see manual about pygame.sprite.collide_mask())
        self.mass = mass  # give sprite a mass -> realistic collisions
        self.X = self.rect.center[0] # assing X position
        self.Y = self.rect.center[1] # assing Y position

        self.friction_positive= mass*friction_coefficent_positive # calculate friction
        self.friction_negative= mass*friction_coefficent_negative # calculate friction

        self.friction_positive_2 = mass*friction_coefficent_positive # calculate friction
        self.friction_negative_2 = mass*friction_coefficent_negative # calculate friction

        self.vx = v[0] # assing vx
        self.vy = v[1] # assing vy

        self.OnPlatform = False
        self.killed = False
        self.tour = True

        self.killed = False
        self.dead = False

class Player(Object):
    def __init__(self, img_path, xy_center, v, mass):
        # ASSIGN CLASS ATTRIBUTES
        super().__init__(img_path, xy_center, v, mass)  # call __init__ of parent class 

        self.movement = " "
        self.jumpingspeed = -20
        self.flip = False
        
    def update(self, platform):
        x= -20
        
        vector_lenght = np.sqrt((self.vx**2))

        if self.movement == "left"and self.X >= 20:
            self.vx = -5

        elif self.movement == "right" and self.X <= 980:
            self.vx = 5

        else:
            if self.vx <= friction_coefficent_positive:
                self.vx = (1/vector_lenght) * self.vx * \
                (vector_lenght-self.friction_positive)
                self.vx = 0
            elif self.vx >= friction_coefficent_positive:

                self.vx = (1/vector_lenght) * self.vx * \
                (vector_lenght-self.friction_negative)
                self.vx = 0

        if self.movement == "shoot":
            pass

        if self.movement == "up":
            self.vy = x
            self.OnPlatform = False
            
            if self.vy <= -12:
                self.movement = " "
                x = 0

        elif self.OnPlatform == True:
            if self.Y < platform.rect.top :
                self.vy = 0
                self.Y = platform.rect.top - 28

            else:
                self.OnPlatform = False
        
        self.vy = self.vy + Grafitation

        self.Y = self.Y + self.vy
        self.X = self.X + self.vx   
        self.rect.center = (self.X, self.Y)

class Platform(Object):
    def __init__(self, img_path, xy_center, v,mass):
        # ASSIGN CLASS ATTRIBUTES
        super().__init__(img_path, xy_center, v,mass) # call __init__ of parent class

class Bullet(Object):
    def __init__(self, img_path, xy_center, v,mass):
        # ASSIGN CLASS ATTRIBUTES
        super().__init__(img_path, xy_center, v,mass) # call __init__ of parent class



class Enemy(Object):
    def __init__(self, img_path, xy_center,v,mass):
        # ASSIGN CLASS ATTRIBUTES
        super().__init__(img_path, xy_center,v,mass) # call __init__ of parent class 
        self.time = 0

    def update(self, platform):
        if self.time == 500:
            self.vx = self.vx * -1
            self.time = 0

        elif self.X <= 10 and self.X >= 990:
            self.vx = self.vx * -1
            self.time = 0
            
        if self.OnPlatform == True:
            if self.Y < platform.rect.bottom - 15 :
                self.vy = 0
                self.Y = platform.rect.top - 15

            else:
                self.OnPlatform = False

        self.time += 1
        
        self.vy = self.vy + Grafitation

        self.Y = self.Y + self.vy
        self.X = self.X + self.vx   
        self.rect.center = (self.X, self.Y)
  
class Game:
    # Main GAME class

    def __init__(self):
        # initialise screen
        pygame.init()
        pygame.font.init()
        self.time_delay = TIME_DELAY
        # create screen which will display everything
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

        pygame.display.set_caption("Jump_and_run")  # Game title

    def quit(self):
        # to quit game
        pygame.quit()
        sys.exit(0)
    
    def play(self):

        ## Player ##
        player= Player(os.path.join("data","FigtherJumpanrunGame.png"),[900,550],[SPEED[0],SPEED[1]],1)

        ## Platform ##
        Platforms_position_list = [[900,900], [900, 600], [800, 500]]
        platforms_list = [0, 0, 0]
        platforms_names_list = ["ground_Panel.png","rectangle_l=60_w=20_col=0_0_0.png","rectangle_l=60_w=20_col=0_0_0.png"]

        for i in range(len(platforms_list)):
            platforms_list[i] = Platform(os.path.join(
                "data", platforms_names_list[i]), Platforms_position_list[i],[0,0],1)

        Platforms = pygame.sprite.Group()
        for c in platforms_list:
            Platforms.add(c)

        ## Enemy ##
        enemys_position_list = [[400,550],[990, 550],[800, 550]]
        enemys_list = [0, 0,0]
        enemys_speed_list = [[0.8,0],[-0.8,0],[-0.8,0]]

        for i in range(len(enemys_list)):
            enemys_list[i] = Enemy(os.path.join(
                "data", "Enemy.png"), enemys_position_list[i],enemys_speed_list[i],1)

        Enemys = pygame.sprite.Group()
        for c in enemys_list:
            Enemys.add(c)

        
        while True:
            IndexOfCollisionPlatform = 0
            IndexOfCollisionPlatform_2 = 0
            Score = 0

            for event in pygame.event.get():

                if pygame.key.get_pressed()[pygame.K_ESCAPE] == True:
                    self.quit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_LEFT:
                        player.movement = "left"   
                        player.flip = True 

                    if event.key == pygame.K_RIGHT:
                        player.movement = "right"
                        player.flip = False
                        
                    if event.key == pygame.K_UP or event.key == pygame.K_w:

                        if player.OnPlatform == True:
                            player.OnPlatform = False 
                            player.movement = "up"

                        else:
                            pass
                    
                    if event.key == pygame.K_LSHIFT:
                        player.movement = "shoot"
                        
                if event.type == pygame.KEYUP:

                    if event.key == pygame.K_LEFT or event.type == pygame.K_a:
                        player.movement = " "
                        
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        player.movement = " "
                        
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        player.movement = " "   

                    if event.key == pygame.K_LSHIFT:
                        player.movement = " "

            self.win.fill((BLUE))

            for i in range(len(platforms_list)):

                self.screen.blit(platforms_list[i].image,platforms_list[i].rect)

                if pygame.sprite.collide_mask(platforms_list[i],player):
                    player.OnPlatform = True 
                    IndexOfCollisionPlatform = i

            for i in range(len(enemys_list)):
                for b in range(len(platforms_list)):
                    if pygame.sprite.collide_mask(platforms_list[b],enemys_list[i]):
                        enemys_list[i].OnPlatform = True
                        IndexOfCollisionPlatform_2 = b

                Enemys.update(platforms_list[IndexOfCollisionPlatform_2])  

            b = 0
            while b < len(enemys_list):
                if pygame.sprite.collide_mask(player,enemys_list[b]):
                    enemys_list.pop(b)
                    Score += 50

                else:
                    b = len(enemys_list)

            Enemys = pygame.sprite.Group()
            for c in enemys_list:
                Enemys.add(c)

            Enemys.draw(self.screen)
         
            self.screen.blit(pygame.transform.flip(player.image, player.flip, False), player.rect)
            player.update(platforms_list[IndexOfCollisionPlatform])

            draw_text("Score" + str(Score), 1000, 1000, BLACK)

            pygame.display.update()

if __name__ == "__main__":
    Game().play()  