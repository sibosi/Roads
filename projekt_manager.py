from settings import *
import pygame

class Button():
    def __init__(self, x, y, image, felulet_meret, size=1):
        if x > 0 or x == 0:
            x = x*Default.TALCA_SIZE+Default.TERKOZ
        elif x < 0:
            x = felulet_meret - abs(x)*Default.TALCA_SIZE-Default.TERKOZ
        self.x = x
        width = image.get_width()
        height = image.get_height()
        if type(size) == type(0):
            self.image = pygame.transform.scale(image, (int(width * size), int(height * size)))
        elif type(size) == type((0, 0, 0)):
            imageX, imageY = size
            self.image = pygame.transform.scale(image, (imageX, imageY))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

pontok_by_kord = {}
pontok = []
class Pont:
    def __init__(self, poz : float):
        x, y = poz
        self.poz = poz
        self.x = x
        self.y = y
        self.kapcsolatok_by_kord = {}
        self.kapcsolatok = []
        if self.poz in pontok_by_kord.keys():
            self.update(pontok_by_kord[self.poz])
        else:
            pontok_by_kord[poz] = self
            pontok.append(self)

    def new(self, new_poz):
        new_pont = pontok_by_kord[new_poz]
        self.kapcsolatok_by_kord[new_poz] = new_pont
        self.kapcsolatok.append(new_pont)
    
    def new2(self, new_poz):
        new_pont = pontok_by_kord[new_poz]
        self.kapcsolatok_by_kord[new_poz] = new_pont
        new_pont.new(self.poz)
        self.kapcsolatok.append(new_pont)
    
    def update(self, new_pont):
        #new_pont.kapcsolatok_by_kord.update(self.kapcsolatok_by_kord)
        #pontok_by_kord[newItem.hely] = self
        self = new_pont

AllFejlecBlokk = []
class FejlecBlokk():
    def __init__(self, hely1 : int, hely2 : int, color : tuple, atlatszo : int = 128) -> None:
        self.hely1 = hely1
        self.hely2 = hely2
        r, g, b = color
        self.color = pygame.Color(r, g, b, atlatszo)
        print(self.color)
        self.rect = (self.hely1*Default.TALCA_SIZE+0.75*Default.TERKOZ, 5, (self.hely2+1)*Default.TALCA_SIZE, Default.TALCA_SIZE-7)
        AllFejlecBlokk.append(self)

    def draw(self, surface):
        shape_surf = pygame.Surface(pygame.Rect(self.rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, self.color, shape_surf.get_rect(), border_radius=15)
        surface.blit(shape_surf, self.rect)

def drawAllFejlecBlokk(surface):
    for item in AllFejlecBlokk:
        item : FejlecBlokk
        item.draw(surface)

def load_vonalak(vonalak):
    tmp = len(vonalak)
    i = 0
    for vonal in vonalak:
        Pont(vonal[0]).new2(Pont(vonal[1]).poz)
        i += 1
        print('Betöltve: ' + str(i//tmp*100) + '%', end='\r')

def kord_igazitas(poz : float, vonalak : list):
    USAGE = False
    for vonal in vonalak:
        tav = tavolsag(poz,vonal[0])
        if tav < Default.KOR_SIZE:
            poz = vonal[0]
            USAGE = True
        tav = tavolsag(poz,vonal[1])
        if tav < Default.KOR_SIZE:
            poz = vonal[1]
            USAGE = True
    return poz, USAGE
