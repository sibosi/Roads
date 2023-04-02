import pygame
from settings import *
from projekt_manager import Button

def Undo(vonalak):
    LEN = len(vonalak)
    if LEN != 0:
        del vonalak[LEN-1]
    return vonalak

def event_settings(surface : pygame.Surface, button : Button, y : int):
    rect = pygame.Rect(button.x-10, y, 160, 80)
    pygame.draw.rect(surface, Color.light_grey, rect, border_radius=15)

