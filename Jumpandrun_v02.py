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
WIN_HEIGHT = 600
WIN_WIDTH = 800

surface = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))

# Colors #
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 215, 0)
DARKGREEN = (0, 205, 155)
BG_COLOR = (0, 205, 155)

# Framerate #
FPS = 20
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

Grafitation = 0.4

## Classes ##

class Object(pygame.sprite.Sprite):
    def __init__(self, img_path, xy_center, v, mass):

        # ASSIGN CLASS ATTRIBUTES
        super().__init__()  # call __init__ of parent class (i.e. of pygame.sprite.Sprite)
        if not os.path.exists(img_path):
            raise Exception(
                "THE FOLLOWING FILE DOES NOT EXIST: {0}".format(img_path))
        self.image = pygame.image.load(str(img_path))  # load image
        self.rect = self.image.get_rect()  # create rectangle containing ball image
        self.rect.center = (int(xy_center[0]), int(xy_center[1]))  # set center coords of ball
        self.mask = pygame.mask.from_surface(self.image)# creates a mask, used for collision detection (see manual about pygame.sprite.collide_mask())
        self.mass = mass  # give sprite a mass -> realistic collisions
        
class Player(Object):
    def __init__(self, img_path, xy_center, v, mass):

        # ASSIGN CLASS ATTRIBUTES
        super().__init__(img_path, xy_center, v, mass)  # call __init__ of parent class (i.e. of pygame.sprite.Sprite)

        self.vx = v[0]
        self.vy = v[1]
        self.friction_positive= mass*friction_coefficent_positive
        self.friction_negative= mass*friction_coefficent_negative


        self.X = self.rect.center[0]
        self.Y = self.rect.center[1]

        self.movement = " "

    def update(self):
        
        vector_lenght = np.sqrt((self.vx**2))

        if self.movement == "left":
            self.vx = -0.1

        elif self.movement == "right":
            self.vx = 0.1

        else:
            if self.vx <= friction_coefficent_positive:
                self.vx = (1/vector_lenght) * self.vx * \
                (vector_lenght-self.friction_positive)
                self.vx = 0
            elif self.vx >= friction_coefficent_positive:

                self.vx = (1/vector_lenght) * self.vx * \
                (vector_lenght-self.friction_negative)
                self.vx = 0

        if self.movement == "up":
            self.vy = -2

        if self.vy < 0:
            self.vy = self.vy + Grafitation
            
        self.Y = self.Y + self.vy
        self.X = self.X + self.vx   
        self.rect.center = (self.X, self.Y)

class Platform(Object):
    def __init__(self, img_path, xy_center, v,mass):

        # ASSIGN CLASS ATTRIBUTES
        super().__init__(img_path, xy_center, v,mass)
        
class Background(Object):
    def __init__(self, img_path, xy_center):
        

        # ASSIGN CLASS ATTRIBUTES
        super().__init__(self, img_path, xy_center) # call __init__ of parent class (i.e. of pygame.sprite.Sprite)
        
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
        pygame.quit()
        sys.exit(0)
    
    def play(self):

        player= Player(os.path.join("data","Test_Enemy.png"),[350,367],[SPEED[0],SPEED[1]],1)

        Platforms_position_list = [[350,400],[325, 250]]
        platforms_list = [0, 0]
        platforms_names_list = ["rectangle_l=900_w=20_col=0_0_0.png","rectangle_l=60_w=20_col=0_0_0.png"]

        for i in range(len(platforms_list)):
            platforms_list[i] = Platform(os.path.join(
                "data", platforms_names_list[i]), Platforms_position_list[i],[0,0],1)

        Platforms = pygame.sprite.Group()
        for c in platforms_list:
            Platforms.add(c)

        while True:

            for event in pygame.event.get():

                if pygame.key.get_pressed()[pygame.K_ESCAPE] == True:
                    self.quit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_LEFT or event.type == pygame.K_a:
                        player.movement = "left"
                        

                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        player.movement = "right"
                        
                    
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        player.movement = "up"
                        

                if event.type == pygame.KEYUP:

                    if event.key == pygame.K_LEFT or event.type == pygame.K_a:
                        player.movement = " "
                        

                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        player.movement = " "
                        

                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        player.movement = " "   

            self.win.fill((BLUE))
            self.screen.blit(player.image,player.rect)

            for i in range(len(platforms_list)):
                pygame.draw.rect(surface, RED, platforms_list[i])

            player.update()

            pygame.display.update()



if __name__ == "__main__":
    Game().play()  
