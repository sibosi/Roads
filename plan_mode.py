import pygame

#Le van-e nyomva a Shift?
def shiftDown(list):
    global shift
    for element in list:
        if element.type == pygame.KEYDOWN:
            if element.dict['key'] == 1073742053 or element.dict['key'] == 1073742049:
                shift = True
    for element in list:
        if element.type == pygame.KEYUP:
            if element.dict['key'] == 1073742053 or element.dict['key'] == 1073742049:
                shift = False
