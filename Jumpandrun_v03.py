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

PATH = Path("data")

# Windows #
WIN_HEIGHT = 800
WIN_WIDTH = 1000

# MIN and MAX Random
BoarderL = 20
BoarderR = 980

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
FPS = 150
TIME_DELAY = int(1000 / FPS)

# Constants #
sx=0
sy=0
SPEED = np.array([sx, sy])
sx_OP = 2
sy_OP = 0
SPEED_OP = np.array([sx_OP,sy_OP])

MAX_PLATFORMS = 10
platforms_list = [0,0,0,0,0,0,0,0,0,0,0]
distance = 30

MAX_BULLETS = 3
bullet_list = [0,0,0]

friction_coefficent_positive = 0.05
friction_coefficent_negative = -0.05
YSpeed = -20

Grafitation = 1

TEXT_SIZE = 20
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
        self.tour = True

        self.killed = False
        self.dead = False

class Player(Object):
    def __init__(self, img_path, xy_center, v, mass,live):
        # ASSIGN CLASS ATTRIBUTES
        super().__init__(img_path, xy_center, v, mass)  # call __init__ of parent class 

        self.movement = " "
        self.movementX = " "
        self.movementY = " "
        self.jumpingspeed = -20
        self.flip = False
        self.live = live
        self.live = 3
        self.killcooldown = 100
        
    def update(self, platform):
        x= -20
        
        vector_lenght = np.sqrt((self.vx**2))

        if self.movementX == "left"and self.X >= BoarderL:
            self.vx = -5

        elif self.movementX == "right" and self.X <= BoarderR:
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

        if self.movementY == "up":
            self.vy = x
            self.OnPlatform = False
            
            if self.vy <= -12:
                self.movementY = " "
                x = 0
            
            if self.vy >= 3:
                x = 0

        elif self.OnPlatform == True:

            if self.Y < platform.rect.top :
                self.vy = 0
                self.Y = platform.rect.top - platform.distance

            else:
                self.OnPlatform = False
        
        self.vy = self.vy + Grafitation

        self.Y = self.Y + self.vy
        self.X = self.X + self.vx   
        self.rect.center = (self.X, self.Y)

class Platform(Object):
    def __init__(self, img_path, xy_center, v,mass, distance):
        # ASSIGN CLASS ATTRIBUTES
        super().__init__(img_path, xy_center, v,mass) # call __init__ of parent class
        self.distance = distance

    def update(self):
        self.Y = self.Y
        self.X = self.X
        self.rect.center = (self.X, self.Y)
class Button(Object):
    def __init__(self, img_path, xy_center, v,mass):
        # ASSIGN CLASS ATTRIBUTES
        super().__init__(img_path, xy_center, v,mass) # call __init__ of parent class

class Heart(Object):
    def __init__(self, img_path, xy_center, v,mass):
        # ASSIGN CLASS ATTRIBUTES
        super().__init__(img_path, xy_center, v,mass) # call __init__ of parent class
        
class Background(Object):
    def __init__(self, img_path, xy_center,v,mass):
        # ASSIGN CLASS ATTRIBUTES
        super().__init__(img_path, xy_center,v,mass) # call __init__ of parent class

class Bullet(Object):
    def __init__(self, img_path, xy_center, v, mass, Bullet_time):
        # ASSIGN CLASS ATTRIBUTES
        super().__init__(img_path, xy_center, v,mass) # call __init__ of parent class
        self.Bullet_time = Bullet_time 
        self.Bullet_time = 40

    def update(self,player):
        if player.movement == "shoot":
            if player.flip == True:
                self.vx = -20
            else:
                self.vx = 20

        else:
            pass

        self.X = self.X + self.vx   
        self.rect.center = (self.X, self.Y)

class Enemy(Object):
    def __init__(self, img_path, xy_center,v,mass,live):
        # ASSIGN CLASS ATTRIBUTES
        super().__init__(img_path, xy_center,v,mass) # call __init__ of parent class 
        self.time = 0
        self.live = live
        self.live = 3

    def update(self, platform):
        if self.time == random.randint(300,600):
            self.vx = self.vx * -1
            self.time = 0

        elif self.X <= BoarderL or self.X >= BoarderR:
            self.vx = self.vx * -1
            self.time = 0
            
        if self.OnPlatform == True:
            self.vy = 0
            self.Y = platform.rect.top - 15

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

        high_score = 0

        ## Player ##
        Players = pygame.sprite.Group() # create Players Sprite Group
        player = Player(os.path.join(PATH,"FigtherJumpanrunGame.png"),[900,550],[SPEED[0],SPEED[1]],1,10)
        Players.add(player)

        ## Bullet ##
        Bullets = pygame.sprite.Group()

        ## Heart ##
        Hearts = pygame.sprite.Group()  # create Hearts Sprite Group
        hearts_position_list = [[450,50],[500,50],[550,50]]

        for i in range(1):
            heart= Heart(os.path.join(
                "data", "Heart.png"), hearts_position_list[i],[0,0],1)

            Hearts.add(heart)

        ## Button ##
        button= Button(os.path.join("data","Playbutton.png"),[500,500],[0,0],1)

        ## Platform ##
        Platform_position_list = [[300,400],[500,500],[500,600],[700,550],[800,600],[850,500],[100,550],[200,640],[250,500],[300,600]]
        for c in range(MAX_PLATFORMS):
            platforms_list[c] = Platform(os.path.join(
                PATH,"Platform.png"), Platform_position_list[c],[0,0],1,22)             

        platforms_list[MAX_PLATFORMS] = Platform(os.path.join(
            PATH, "ground_Panel.png"), [900,900],[0,0],1,28)

        # create Platform Sprite Group
        Platforms = pygame.sprite.Group()  # create Platforms Sprite Group
        for c in platforms_list:
            Platforms.add(c)   

        ## Enemy ##
        Enemys = pygame.sprite.Group() # create Enemys Sprite Group
        Enemys_xSpeed = 1

        for i in range(4):
            Enemys_xSpeed = Enemys_xSpeed * -1
            randomXSPEED = Enemys_xSpeed * 1
            randomXE_position = random.randint(20,800)

            enemy = Enemy(os.path.join(PATH, "Enemy.png"), [randomXE_position, 750],[randomXSPEED, 0],1, 3)
            Enemys.add(enemy)

        ## Backgrounds ##
        backgrounds_list= [0, 0, 0]
        backgrounds_names_list = ["Planet_Meriec.png","Levels.png","END.png"]
        backgrounds_position_list = [[500,500],[500,500],[500,500]]

        for i in range(len(backgrounds_list)):
            backgrounds_list[i] = Background(os.path.join(
                "data", backgrounds_names_list[i]), backgrounds_position_list[i],[0,0],1)

        Backgrounds = pygame.sprite.Group() #create Backgrounds Sprite Group
        for c in backgrounds_list:
            Backgrounds.add(c)

        countdown = 1

        while True:
            # KEY EVENTS
            for event in pygame.event.get():

                clickdetection = Rect(400,450,200,100)

                if pygame.key.get_pressed()[pygame.K_ESCAPE] == True:
                    self.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if clickdetection.collidepoint(event.pos) == 1:
                        IndexOfCollisionPlatform = 0
                        GameOver = False
                        
                        Score = 0
                        livecountdown = 10

                        for c in range(len(platforms_list)-1):
                            for i in range(len(platforms_list)-1):
                                if pygame.sprite.collide_mask(platforms_list[i],platforms_list[c]):
                                    while True:
                                        if pygame.sprite.collide_mask(platforms_list[i],platforms_list[c]) != True:
                                            print(platforms_list[c].Y)
                                            break
                                        platforms_list[c].Y = random.randint(300,650)
                                        platforms_list[c].X = random.randint(200,800)
                                    platforms_list[c].update()
                                    
                        while True:

                            IndexOfCollisionPlatform = 0
                            IndexOfCollisionPlatform_2 = 0
                            pygame.time.delay(TIME_DELAY)
                            
                            for event in pygame.event.get():

                                if pygame.key.get_pressed()[pygame.K_ESCAPE] == True:
                                    self.quit()

                                if event.type == pygame.KEYDOWN:

                                    if event.key == pygame.K_LEFT:
                                        player.movementX = "left"   
                                        player.flip = True 

                                    if event.key == pygame.K_RIGHT:
                                        player.movementX = "right"
                                        player.flip = False


                                    if pygame.key.get_pressed()[pygame.K_r] == True:
                                        Game().play()
                                    
                                    if event.key == pygame.K_UP :

                                        if player.OnPlatform == True:
                                            player.OnPlatform = False 
                                            player.movementY = "up"

                                        else:
                                            pass
                                    
                                    if event.key == pygame.K_w:
                                        player.movement = "shoot"
                                        bullet = Bullet(os.path.join(PATH,"Bullet.png"),[player.X, player.Y],[0,0],1,0)
                                        if len(Bullets) < 5:
                                            Bullets.add(bullet)  
                                        
                                if event.type == pygame.KEYUP:

                                    if event.key == pygame.K_LEFT or event.type == pygame.K_a:
                                        player.movementX = " "
                                        
                                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                                        player.movementX = " "
                                        
                                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                                        player.movementY = " "   

                                    if event.key == pygame.K_LSHIFT:
                                        player.movement = " "


                            player.OnPlatform = False

                            for i in range(len(platforms_list)):
                                if pygame.sprite.collide_mask(platforms_list[i],player):
                                    player.OnPlatform = True 
                                    IndexOfCollisionPlatform = i

                            for enemy in Enemys:
                                for b in range(len(platforms_list)):
                                    if pygame.sprite.collide_mask(platforms_list[b],enemy):
                                        enemy.OnPlatform = True
                                        IndexOfCollisionPlatform_2 = b

                                for player in Players:
                                    if pygame.sprite.collide_mask(enemy, player):
                                        livecountdown -= countdown
                                        if livecountdown <= 0:
                                            countdown = 0

                                        print(livecountdown)

                                        if livecountdown == 0:
                                            Hearts.remove(heart)
                                            player.live -= 1 
                                            enemy.live -= 1 
                                            countdown = 1
                                            livecountdown = 5

                                        if player.live == -1 :
                                            Players.remove(player)
                                            GameOver = True

                                    
                                    player.killcooldown -= 1

                                Enemys.update(platforms_list[IndexOfCollisionPlatform_2])  

                            for bullet in Bullets:
                                for enemy in Enemys:
                                    if pygame.sprite.collide_mask(bullet,enemy):
                                        Bullets.remove(bullet)
                                        enemy.live -= 1

                                        if enemy.live == 0:
                                            Enemys.remove(enemy)
                                            Score += 50

                                bullet.Bullet_time -= 1

                                if bullet.Bullet_time == 0:
                                    Bullets.remove(bullet)

                                bullet.update(player)
 
                            if len(Enemys) < 4:
                                Enemys_xSpeed = Enemys_xSpeed * -1
                                randomXSPEED = Enemys_xSpeed * 1
                                randomXE_position = random.randint(20,980)

                                enemy = Enemy(os.path.join(PATH, "Enemy.png"), [randomXE_position, 550],[randomXSPEED, 0],1, 3)
                                Enemys.add(enemy)

                            if GameOver == True:
                                self.screen.blit(backgrounds_list[2].image,backgrounds_list[2].rect)

                                draw_text("Score" + " " + str(Score), 490, 500, WHITE)
                                draw_text("To Quit Press ESC", 460, 600, WHITE)
                                draw_text("GAME OVER", 480, 400, WHITE)
                                draw_text("To Restart press R", 480, 700, WHITE)

                                if Score > high_score:
                                    high_score = Score

                                draw_text("High Score" + " " + str(high_score), 470, 550, WHITE)
                                
                            else:
                                self.screen.blit(backgrounds_list[1].image,backgrounds_list[1].rect)
                                Platforms.draw(self.screen)
                                self.screen.blit(pygame.transform.flip(player.image, player.flip, False), player.rect)
                                Enemys.draw(self.screen)
                                Bullets.draw(self.screen)
                                Hearts.draw(self.screen)
                                
                                player.update(platforms_list[IndexOfCollisionPlatform])

                                draw_text("Score" + " " + str(Score), 890, 20, WHITE)

                            pygame.display.update()

                self.screen.blit(backgrounds_list[0].image,backgrounds_list[0].rect)
                self.screen.blit(button.image,button.rect)

                pygame.display.update()

if __name__ == "__main__":
    Game().play()  