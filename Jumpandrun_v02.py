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

# Windows #
WIN_HEIGHT = 600
WIN_WIDTH = 800

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
sy=-20
SPEED = np.array([sx, sy])
sx_OP = 2
sy_OP = 0
SPEED_OP = np.array([sx_OP,sy_OP])

friction_coefficent = 0.05
grafitation = 1

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
        
        self.friction= mass*friction_coefficent

        self.X = self.rect.center[0]
        self.Y = self.rect.center[1]
        
class Player(Object):
    def __init__(self, img_path, xy_center, v, mass):

        # ASSIGN CLASS ATTRIBUTES
        super().__init__(img_path, xy_center, v, mass)  # call __init__ of parent class (i.e. of pygame.sprite.Sprite)

    def update():

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT or event.type == pygame.K_a:
                    print(1)

                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    print(2)

            if event.type == pygame.KEYUP:

                if event.key == pygame.K_LEFT or event.type == pygame.K_a:
                    print()

                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    print()



class Platform(Object):
    def __init__(self, img_path, xy_center,v):

        # ASSIGN CLASS ATTRIBUTES
        super().__init__(self, img_path, xy_center, v) # call __init__ of parent class (i.e. of pygame.sprite.Sprite)

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

        player= Player(os.path.join("data","Test_Enemy.png"),[300,300],[SPEED[0],SPEED[1]],1)

        pygame.display.update()

        while True:


            if pygame.key.get_pressed()[pygame.K_ESCAPE] == True:
                self.quit()

            self.win.fill((BLUE))
            self.screen.blit(player.image,player.rect)

            Player.update()

            pygame.display.update()



if __name__ == "__main__":
    Game().play()  
