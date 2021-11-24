import os
from PIL import Image, ImageDraw
from pathlib import Path
import sys
print(os.getcwd())

# CONSTANTS
PATH = Path("data/")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 215, 0)
BLACKBIG = (0, 0, 0)
ORANGE = (225, 165, 0)
BLUEVIOLETT = (138, 43, 226)
YELLOW = (255, 215, 0)
DARKGREEN = (0, 205, 155)
BG_COLOR = (0, 205, 155)


def draw_bmp_Platform(lenght,widht, color):
    # CREATE BALL IMAGE (if does not exist yet)
    if not os.path.exists(PATH):
        os.makedirs(PATH)

    file_path = Path(
        f"{PATH}/rectangle_l={lenght}_w={widht}_col={str(color).replace(' ','').replace(',','_').replace(')','').replace('(','')}.png")

    if not os.path.isfile(file_path):
        img = Image.new('RGBA', (lenght, widht), (255, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rectangle((0, 0, lenght, widht), fill=color)
        img.save(file_path, 'PNG')


if __name__ == "__main__":
    draw_bmp_Platform(60,20, BLACK)