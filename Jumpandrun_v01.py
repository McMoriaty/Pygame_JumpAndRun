from typing import Tuple
import pygame
import time
import math
import sys
import numpy as np
import random
import os

from numpy.core.numeric import True_
from pathlib import Path
from pygame import Rect, constants
from PIL import Image, ImageDraw
from pygame.key import get_pressed
from pygame.key import get_mods

### CONSTANTS ###

# Windows #
WIN_HEIGHT = 1000
WIN_WIDTH = 1800

# Colors #
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 215, 0)
DARKGREEN = (0, 205, 155)
BG_COLOR = (0, 205, 155)

# Font #
pygame.init()
pygame.font.init()

TEXT_SIZE = 25
size = [WIN_WIDTH, WIN_HEIGHT]
screen = pygame.display.set_mode(size)

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
HIGH = 700
friction_coefficent = 0.05
grafitation = 1
N_grafitation =-1

# Classes #
class Player(pygame.sprite.Sprite):
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
        
        self.vx = v[0]
        self.vy = v[1]

        self.X= self.rect.center[0]
        self.Y= self.rect.center[1]
        
        self.jumping = False
        self.jumpCount = 10
        self.isJump = False
        self.topjump= False

        self.isOnPlatform = False
        self.isOnGround = False

        self.runCount= 5
        self.runforward =False
        self.runback = False
        self.kneeing = False
        self.isshooting = False

    def shoot(self):
        pass

    def jump(self): # Function for jumping
        y=20
        if self.isJump == True and not self.isOnPlatform:
            self.vy += grafitation 

            if self.vy == 0:
                self.topjump = True
                grafitation*-1

            if self.vy >= y:
                self.vy = -y
                self.Y = HIGH
                self.isJump = False

            self.Y = self.Y + self.vy
            self.rect.center = (self.X, self.Y)

        else:
            self.isJump = False 
            self.topjump = False
            
    def walk(self): # Function for walking

        if self.runforward == True:
            self.vx += 5
                
            self.X = self.X + self.vx

            self.rect.center = (self.X, self.Y)

        if self.runback == True:
            self.vx -= 5
 
            self.X = self.X + self.vx
            
            self.rect.center = (self.X, self.Y)

        if self.runforward == False or self.runback == False:
            self.vx = 0 
            self.X = self.X + self.vx
            self.rect.center = (self.X, self.Y)
class Background(pygame.sprite.Sprite):
    def __init__(self, img_path, xy_center):
        super().__init__()

        # ASSIGN CLASS ATTRIBUTES
        if not os.path.exists(img_path):  # check if folder of image exists
            raise Exception(
                "THE FOLLOWING FILE DOES NOT EXIST: {0}".format(img_path))
        self.image = pygame.image.load(str(img_path))  # load image
        self.rect = self.image.get_rect()  # create rectangle containing ball image
        self.rect.center = (int(xy_center[0]), int(xy_center[1]))  # set center coords of ball
class Button(pygame.sprite.Sprite):
    def __init__(self, img_path, xy_center):
        super().__init__()

        # ASSIGN CLASS ATTRIBUTES
        if not os.path.exists(img_path):  # check if folder of image exists
            raise Exception(
                "THE FOLLOWING FILE DOES NOT EXIST: {0}".format(img_path))
        self.image = pygame.image.load(str(img_path))  # load image
        self.rect = self.image.get_rect()  # create rectangle containing ball image
        self.rect.center = (int(xy_center[0]), int(xy_center[1]))  # set center coords of ball
class Platform(pygame.sprite.Sprite):
    def __init__(self, img_path, xy_center,v,lenght):
        super().__init__()

        # ASSIGN CLASS ATTRIBUTES
        if not os.path.exists(img_path):  # check if folder of image exists
            raise Exception(
                "THE FOLLOWING FILE DOES NOT EXIST: {0}".format(img_path))
        self.image = pygame.image.load(str(img_path))  # load image
        self.rect = self.image.get_rect()  # create rectangle containing ball image
        self.rect.center = (int(xy_center[0]), int(xy_center[1]))  # set center coords of ball
        self.mask = pygame.mask.from_surface(self.image)# creates a mask, used for collision detection (see manual about pygame.sprite.collide_mask())
        self.lenght = lenght

        self.X= self.rect.center[0]
        self.Y= self.rect.center[1]

class Opponent(pygame.sprite.Sprite):
    def __init__(self, img_path, xy_center, v, mass):
        super().__init__()  # call __init__ of parent class (i.e. of pygame.sprite.Sprite)

        # ASSIGN CLASS ATTRIBUTES
        if not os.path.exists(img_path):
            raise Exception("THE FOLLOWING FILE DOES NOT EXIST: {0}".format(img_path))
        self.image = pygame.image.load(str(img_path))  # load image
        self.rect = self.image.get_rect()  # create rectangle containing ball image
        self.rect.center = (int(xy_center[0]), int(xy_center[1]))  # set center coords of ball
        self.mask = pygame.mask.from_surface(self.image)# creates a mask, used for collision detection (see manual about pygame.sprite.collide_mask())
        self.mass= mass

        self.friction= mass*friction_coefficent
        
        self.vx = v[0]
        self.vy = v[1]

        self.X= self.rect.center[0]
        self.Y= self.rect.center[1]

        self.killed = False
        self.tour = True

    def dead(self,Player):
        if Player.topjump == True:
            print("dead")
            Player.topjump = False
            self.killed= True

        else:
            pass

    def walk(self):
        pass
 
        """turn = 0
        
        vector_lenght = np.sqrt((self.vx**2) + (self.vy**2))

        self.vx = (1/vector_lenght) * self.vx * \
            (vector_lenght-self.friction)
        self.vy = (1/vector_lenght) * self.vy * \
            (vector_lenght-self.friction)

    
        if turn <= 10:
            self.vx = (self.vx+sx_OP)*-1
            turn += 1

        elif turn > 10:
            self.vx = (self.vx-sx_OP)**2
            turn += 1

        elif turn > 20:
            turn = 0

        print(turn)
        print(self.vx)"""

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
        self.start = False
        
        pygame.display.set_caption("Jump_and_run")  # Game title

    def quit(self):
        pygame.quit()
        sys.exit(0)

    def play(self):

        player= Player(os.path.join("data","Test_Enemy.png"),[900,HIGH],[SPEED[0],SPEED[1]],1)       

        buttons= Button(os.path.join("data","Playbutton.png"),[900,700])
        buttons_list= [buttons]

        Buttons = pygame.sprite.Group()
        for c in buttons_list:
            Buttons.add(c)
        
        background= Background(os.path.join("data","Planet_Meriec.png"),[900,500])
        backgrounds_list= [background]

        Backgrounds = pygame.sprite.Group()
        for c in backgrounds_list:
            Backgrounds.add(c)

        opponent= Opponent(os.path.join("data","explosions_10.png"),[300,HIGH],[SPEED_OP[0],SPEED_OP[1]],1)
        opponents_list= [opponent]

        Platforms_position_list = [[900,600],[1500,600]]
        platforms_list = [0, 0]

        for i in range(len(platforms_list)):
            platforms_list[i] = Platform(os.path.join(
                "data", "Test_Platform.png"), Platforms_position_list[i],[0],[100])

        Platforms = pygame.sprite.Group()
        for c in platforms_list:
            Platforms.add(c)
        
        # GAME PERMANENT LOOP
        while True:
            # KEY EVENTS
            for event in pygame.event.get():

                clickdetection = Rect(800,650,200,100)

                if pygame.key.get_pressed()[pygame.K_ESCAPE] == True:
                    self.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if clickdetection.collidepoint(event.pos) == 1:

                        while True:
                            pygame.time.delay(TIME_DELAY)

                            # KEY EVENTS
                            for event in pygame.event.get():

                                if pygame.key.get_pressed()[pygame.K_ESCAPE] == True:
                                    self.quit()

                                # to find out the position of the mouse click
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    pass

                                if event.type == pygame.KEYDOWN:

                                    if event.key == pygame.K_LEFT or event.type == pygame.K_a:
                                        player.runback = True 

                                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                                        player.runforward = True
                                    
                                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                                        player.isJump = True
                                        player.isOnPlatform = False 
                                        player.isOnGroud = False
           
                                    if event.key == pygame.K_SPACE == True:
                                        player.isshooting = True

                                if event.type == pygame.KEYUP:

                                    if event.key == pygame.K_LEFT or event.type == pygame.K_a:
                                        player.runback = False

                                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                                        player.runforward = False

                                    if event.key == pygame.K_SPACE:
                                        player.isshooting = False

                                if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]== True:
                                    player.kneeing = True

                            for i in range(len(opponents_list)):
                                if pygame.sprite.collide_mask(opponent, player):
                                    opponent.dead(player)

                                if opponent.killed == True:
                                    opponents_list.pop(i)

                            vy=0
                            for i in range(len(platforms_list)):
                                player.isOnPlatform = False
                                player.isOnGround = True
                                X_Position_1 = platforms_list[i].X - 80
                                X_Position_2 = platforms_list[i].X + 100

                                if pygame.sprite.collide_mask(platforms_list[i],player):
                                    player.isOnGround = False
                                    if player.vy > 0:
                                        player.vy = vy
                                        player.vy = 0
                                        player.isOnPlatform = True
                                        player.isJump = False

                                    if  player.X <= X_Position_1:
                                        player.vy = vy
                                        player.isOnPlatform = False
                                        player.isJump = True
                                    
                                    elif player.X >= X_Position_2 :
                                        player.vy = vy
                                        player.isOnPlatform = False
                                        player.isJump = True

                                #print(self.Y)
                                #print(Y_Position_2)

                            opponent.walk()

                            Opponents = pygame.sprite.Group()
                            for c in opponents_list:
                                Opponents.add(c)

                            self.win.fill((BLUE))
                            Opponents.draw(self.screen)

                            player.jump()
                            player.shoot()
                            player.walk()
                            Platforms.draw(self.screen)
                            self.screen.blit(player.image,player.rect)

                            pygame.display.update()

                Backgrounds.draw(self.screen)
                Buttons.draw(self.screen)

                pygame.display.update()
                

if __name__ == "__main__":
    Game().play()    