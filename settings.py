import ctypes
from math import sqrt
import pygame
from path import *
import screeninfo

PLAN_MODE = False

class Color():
    green_grass = (63,152,107)
    red = (255, 0, 0)
    green = (0, 255, 8)
    blue = (0, 0, 255)
    white = (255, 255, 255)
    black = (0, 0, 0)
    cian = (0, 255, 255)
    yellow = (255, 255, 0)
    pink = (255, 0, 255)
    kiwi = (161, 245, 66)
    grey = (241, 241, 241)
    wood = (181, 136, 95)
    light_grey = (148, 160, 179)

class MonitorMode():
    big = -20, -125
    normal = -50, -125
    small = -1000, -125
    half = -700, -125


class Default():
    MONITOR_MODE = MonitorMode.normal

    ZOOM = 2
    TALCA_SIZE = 110#110
    TERKOZ = 30#20
    VONAL_SIZE = int(1+ZOOM*0.5)
    KOR_SIZE = int(9+ZOOM*1.5)

    KIV_VONAL = Color.kiwi
    NOR_VONAL = Color.blue
    KIV_PONT = Color.cian
    NOR_PONT = Color.red
    HATTER = Color.green_grass

root = screeninfo.get_monitors()
i = root[0]
SCREEN_SIZE = i.width, i.height
print('SCREEN_SIZE=', SCREEN_SIZE)

window_icon = pygame.image.load(IMAGE_PATH / 'arrow.png')
image_undo = pygame.image.load(IMAGE_PATH / 'undo.png')#.convert_alpha()
image_save = pygame.image.load(IMAGE_PATH / 'save.png')
image_open = pygame.image.load(IMAGE_PATH / 'explorer.png')
image_settings = pygame.image.load(IMAGE_PATH / 'settings.png')



def tavolsag(a,b):
    ax, ay = a
    bx, by = b
    tav = sqrt((bx-ax)**2+(by-ay)**2)
    return tav
