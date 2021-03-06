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
WIN_HEIGHT = 960
WIN_WIDTH = 1728

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

enemy_movement_positive = 10
enemy_movement_negative = 10

Grafitation = 2

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
        
class Player(Object):
    def __init__(self, img_path, xy_center, v, mass):
        # ASSIGN CLASS ATTRIBUTES
        super().__init__(img_path, xy_center, v, mass)  # call __init__ of parent class 

        self.movement = " "
        self.jumpingspeed = -20
        
    def update(self, platform):
        x= -20
        
        vector_lenght = np.sqrt((self.vx**2))

        if self.movement == "left":
            self.vx = -5

        elif self.movement == "right":
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

        if self.movement == "up":
            self.vy = x
            print("hello")
            self.OnPlatform = False
            
            if self.vy <= -12:
                self.movement = " "
                x = 0

        if self.OnPlatform == True:
            self.vy = 0
            self.Y = platform.rect.top - 20

        self.vy = self.vy + Grafitation

        self.Y = self.Y + self.vy
        self.X = self.X + self.vx   
        self.rect.center = (self.X, self.Y)

class Platform(Object):
    def __init__(self, img_path, xy_center, v,mass):
        # ASSIGN CLASS ATTRIBUTES
        super().__init__(img_path, xy_center, v,mass) # call __init__ of parent class

class Button(Object):
    def __init__(self, img_path, xy_center, v,mass):
        # ASSIGN CLASS ATTRIBUTES
        super().__init__(img_path, xy_center, v,mass) # call __init__ of parent class
        
class Background(Object):
    def __init__(self, img_path, xy_center,v,mass):
        # ASSIGN CLASS ATTRIBUTES
        super().__init__(img_path, xy_center,v,mass) # call __init__ of parent class

class Enemy(Object):
    def __init__(self, img_path, xy_center,v,mass):
        # ASSIGN CLASS ATTRIBUTES
        super().__init__(img_path, xy_center,v,mass) # call __init__ of parent class 

    def update(self):

        vector_lenght = np.sqrt((self.vx**2))

        if self.vx <= friction_coefficent_positive:
            self.vx = (1/vector_lenght) * self.vx * \
            (vector_lenght-self.friction_positive_2)

        elif self.vx >= friction_coefficent_positive:
            self.vx = (1/vector_lenght) * self.vx * \
            (vector_lenght-self.friction_negative_2)
            
        if  self.vx >= 10.9:
            self.vx = 10*-1

        if self.vx >= -9 and self.vx <= 0:
            self.vx = -10*-1

        if self.OnPlatform == True:
            self.vy = 0

        else:
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

        ## Button ##

        button= Button(os.path.join("data","Playbutton.png"),[900,700],[0,0],1)

        ## Player ##

        player= Player(os.path.join("data","Test_Enemy.png"),[900,550],[SPEED[0],SPEED[1]],1)

        ## Enemy ##

        enemys_position_list = [[400,550],[1300, 550]]
        enemys_list = [0, 0]
        enemys_names_list = ["Enemy.png","Enemy.png"]
        enemys_speed_list = [[10,0],[-10,0]]

        for i in range(len(enemys_list)):
            enemys_list[i] = Enemy(os.path.join(
                "data", enemys_names_list[i]), enemys_position_list[i],enemys_speed_list[i],1)

        Enemys = pygame.sprite.Group()
        for c in enemys_list:
            Enemys.add(c)

        ## Platform ##

        Platforms_position_list = [[900,800],[900, 500]]
        platforms_list = [0, 0]
        platforms_names_list = ["ground_Panel.png","rectangle_l=60_w=20_col=0_0_0.png"]

        for i in range(len(platforms_list)):
            platforms_list[i] = Platform(os.path.join(
                "data", platforms_names_list[i]), Platforms_position_list[i],[0,0],1)

        Platforms = pygame.sprite.Group()
        for c in platforms_list:
            Platforms.add(c)

        ## Backgrounds ##

        backgrounds_list= [0, 0]
        backgrounds_names_list = ["Planet_Meriec.png","Levels.png"]
        backgrounds_position_list = [[900,500],[900,500]]

        for i in range(len(backgrounds_list)):
            backgrounds_list[i] = Background(os.path.join(
                "data", backgrounds_names_list[i]), backgrounds_position_list[i],[0,0],1)

        Backgrounds = pygame.sprite.Group()
        for c in backgrounds_list:
            Backgrounds.add(c)

        while True:
            # KEY EVENTS
            for event in pygame.event.get():

                clickdetection = Rect(800,650,200,100)

                if pygame.key.get_pressed()[pygame.K_ESCAPE] == True:
                    self.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if clickdetection.collidepoint(event.pos) == 1:
                        IndexOfCollisionPlatform = 0
                        while True:

                            for event in pygame.event.get():

                                if pygame.key.get_pressed()[pygame.K_ESCAPE] == True:
                                    self.quit()

                                if event.type == pygame.KEYDOWN:

                                    if event.key == pygame.K_LEFT or event.type == pygame.K_a:
                                        player.movement = "left"    

                                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                                        player.movement = "right"
                                        
                                    if event.key == pygame.K_UP or event.key == pygame.K_w and player.movement == " ":
                                        player.OnPlatform = False 
                                        player.movement = "up"
                                        

                                if event.type == pygame.KEYUP:

                                    if event.key == pygame.K_LEFT or event.type == pygame.K_a:
                                        player.movement = " "
                                        
                                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                                        player.movement = " "
                                        
                                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                                        player.movement = " "   

                            self.screen.blit(backgrounds_list[1].image,backgrounds_list[1].rect)

                            for i in range(len(platforms_list)):

                                self.screen.blit(platforms_list[i].image,platforms_list[i].rect)

                            if pygame.sprite.collide_mask(platforms_list[i],player):
                                player.OnPlatform = True 
                                IndexOfCollisionPlatform = i

                            else:
                                if player.OnPlatform == False:
                                    Player.vy = 0

                            for i in range(len(enemys_list)):

                                if pygame.sprite.collide_mask(platforms_list[i],enemys_list[i]):
                                    enemys_list[i].OnPlatform = True


                            Enemys = pygame.sprite.Group()
                            for c in enemys_list:
                                Enemys.add(c)

                            Enemys.draw(self.screen)

                            Enemys.update()
                        
                            player.update(platforms_list[IndexOfCollisionPlatform])

                            self.screen.blit(player.image,player.rect)

                            print(player.OnPlatform)
                            pygame.display.update()

                self.screen.blit(backgrounds_list[0].image,backgrounds_list[0].rect)
                self.screen.blit(button.image,button.rect)

                pygame.display.update()

if __name__ == "__main__":
    Game().play()  