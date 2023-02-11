from datetime import datetime
import os
from fileOpen import *
import pathlib
from time import sleep
import pygame
from math import sqrt
import ctypes#A képernyő nagyságát adja meg

ora = pygame.time.Clock()
konyvtar = 'Roads tervek'
shift = False
openedFileName = None

#file inportálása:
path = str(str(pathlib.Path(__file__).parent.resolve())+('\{0}'.format(konyvtar)))
newpath = r''+ path# megadja az aktuális mappa elérési útját
if not os.path.exists(newpath):# ha nincs ilyen mappa, akkor készít egyet
    os.makedirs(newpath)

#actual path
actual_path = str(pathlib.Path(__file__).parent.resolve()) + '\\'

#font
pygame.font.init()
myfont = pygame.font.SysFont('Calibri', 30)

#colors:
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

#monitorMode:
big = -20, -125
normal = -50, -125
small = -1000, -125
half = -700, -125

monitorMode = normal

#settings
zoom = 2
talca_size = 110#110
terkoz = 30#20
vonal_size = int(1+zoom*0.5)
kor_size = int(9+zoom*1.5)

kivVonal = Color.kiwi
norVonal = Color.blue
kivPont = Color.cian
norPont = Color.red
hatter = Color.green_grass


def elementInDict(element, dict):
    keys = []
    for key in dict.keys():
        keys.append(key)
    if element in keys:
        return True
    else:
        return False

def newItemInDict(dict, key, value):
    if elementInDict(key, dict):
        dict[key] = value
    else:
        tmp = {
            key : value
        }
        dict.update(tmp)
    return dict

def listTxtFiles(path = path, format = '.txt'):
    mappaLista = os.listdir(path)
    tmp = mappaLista
    mappaLista = []
    for file in tmp:
        leng = len(file)
        if file[(leng-4):] == format:
            mappaLista.append(file)
    return mappaLista

def makeDict(keys, valuen):
    dict = {}
    for i in range(len(keys)):
        dict.update({ keys[i] : valuen[i]})
    return dict

def tavolsag(a,b):
    x1, y1 = a
    x2, y2 = b
    tav = sqrt((x2-x1)**2+(y2-y1)**2)
    return tav

def eventInList(event, list):
    i = -1
    tmp = True
    final = False
    for element in list:
        if tmp:
            if element.type == event:
                final = True
                tmp = False
            i+= 1
    if final:
        global es
        es = list[i]
    return final

def monitorSize():
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    return screensize

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

def saveProjekt(infosDict, vonalak, name = False, openedFileName = None):
    if not name:
        file = open(os.path.expanduser(os.path.join(path, 'elozoRajz' + '.txt')), 'w')
    #os.path.expanduser(os.path.join("~/Desktop",boyka + ".txt"))
    tmp = ''
    for n in vonalak:
        for i in n:
            tx, ty = i
            tmp = tmp+str(tx)+' '+str(ty)+','
        tmp = tmp[:len(tmp)-1]
        tmp = tmp+'/'
    tmp = tmp[:len(tmp)-1]

    infosDict = newItemInDict(infosDict, 'created', str(datetime.now()))
    infos = ''
    for key, value in infosDict.items():
        infos = infos + key + ':' + value + '\n'

    tmp = infos + tmp
    if not name:
        file.write(tmp)
    file = open(os.path.expanduser(os.path.join(path, 'e' + '.txt')), 'w')
    file.write(tmp)
    file.close()

    if name:
        print('SAVE FILE def START')
        print(path, tmp, openedFileName)
        saveFile(r'' + path, tmp)
        print('SAVE FILE def START')


pontok = []
ids = {}
class Pont:
    def __init__(self, poz):
        x, y = poz
        self.poz = poz
        self.x = x
        self.y = y
        self.kapcsolat = []
        self.hely = len(pontok)# Megmondja a listában elfoglalt helyét
        pontok.append(self)
        if poz in ids.keys():
            self.update(ids[poz])
        ids.update({poz : self})

    def new(self, hely):
        self.kapcsolat.append(hely)
    
    def new2(self, hely):
        new = pontok[hely]
        self.kapcsolat.append(hely)
        new.new(self.hely)
    
    def update(self, newItem):
        self.kapcsolat += newItem.kapcsolat
        pontok[newItem.hely] = self
        del newItem


class Button():
    def __init__(self, x, y, image, felulet_meret, size=1):
        if x > 0 or x == 0:
            x = x*talca_size+terkoz
        elif x < 0:
            x = felulet_meret - abs(x)*talca_size-terkoz
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

AllFejlecBlokk = []
class FejlecBlokk():
    def __init__(self, hely1 : int, hely2 : int, color : tuple, atlatszo : int = 128) -> None:
        self.hely1 = hely1
        self.hely2 = hely2
        r, g, b = color
        self.color = pygame.Color(r, g, b, atlatszo)
        print(self.color)
        self.rect = (self.hely1*talca_size+0.75*terkoz, 5, (self.hely2+1)*talca_size, talca_size-7)
        AllFejlecBlokk.append(self)

    def draw(self, surface):
        shape_surf = pygame.Surface(pygame.Rect(self.rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, self.color, shape_surf.get_rect(), border_radius=15)
        surface.blit(shape_surf, self.rect)

def drawAllFejlecBlokk(surface):
    for item in AllFejlecBlokk:
        item : FejlecBlokk
        item.draw(surface)

def load(vonalak):
    tmp = len(vonalak)
    i = 0
    for vonal in vonalak:
        Pont(vonal[0]).new2(Pont(vonal[1]).hely)
        i += 1
        print('Betöltve: ' + str(i//tmp*100) + '%', end='\r')

def Undo(vonalak):
    LEN = len(vonalak)
    if LEN != 0:
        del vonalak[LEN-1]
    return vonalak

def event_settings(surface : pygame.Surface, button : Button, y : int):
    rect = pygame.Rect(button.x-10, y, 160, 80)
    pygame.draw.rect(surface, Color.light_grey, rect, border_radius=15)

loading = 0
bestTav = -2
bestVonal = []
def plan(poz1, poz2, tav=0, megtettHelyek = []):
    global loading
    global bestTav
    global bestVonal
    item = ids[poz1]
    win = ids[poz2]

    if loading == 5:
        loading = 0
    loading += 1
    #print('Az útvonal kiszámítása' + loading*'.' + str(loading), end='\r')
    if tav < bestTav or bestTav < 0:
        if item not in megtettHelyek:
            megtettHelyek.append(item)
            if item == win:
                if bestTav > tav or bestTav < 0:
                    bestTav = tav
                    bestVonal = megtettHelyek[:]
            tmp = tav
            for k in item.kapcsolat:
                tav = tmp
                k = pontok[k]
                if k not in megtettHelyek:
                    tav += tavolsag(item.poz, k.poz)
                    plan(k.poz, poz2, tav, megtettHelyek[:])

def main(dict = {}, v = [], openedFileName = None):
    pygame.init()
    X1, Y1 = monitorSize()
    tmpX, tmpY = monitorMode
    felulet_meret_x = X1 + tmpX
    felulet_meret_y = Y1 + tmpY
    del tmpX
    del tmpY

    window_icon = pygame.image.load(actual_path + 'arrow.png')
    image_undo = pygame.image.load(actual_path + 'undo.png')#.convert_alpha()
    image_save = pygame.image.load(actual_path + 'save.png')
    image_open = pygame.image.load(actual_path + 'explorer.png')
    image_settings = pygame.image.load(actual_path + 'settings.png')
    mode_setings = False

    fo_felulet = pygame.display.set_mode((felulet_meret_x,felulet_meret_y))
    if openedFileName == None:
        pygame.display.set_caption('Roads')
    else:
        pygame.display.set_caption('Roads - ' + openedFileName)
    pygame.display.set_icon(window_icon)
    icon_size = (talca_size-15, talca_size-15)
    button_open = Button(0, 10, image_open, felulet_meret_x, icon_size)
    button_undo = Button(1, 10, image_undo, felulet_meret_x, icon_size)
    button_save = Button(2, 10, image_save, felulet_meret_x, icon_size)
    button_settings = Button(-1, 10, image_settings, felulet_meret_x, icon_size)

    FejlecBlokk(0, 2, Color.wood)

    egerAllapot = ""
    vonalak = v[:]
    infosDict = dict
    kivalasztott = []
    TERV = False
    global bestTav
    global bestVonal

    if v != []:
        load(vonalak)

    while True:
        global bestVonal
        fo_felulet.fill(hatter)
        pygame.draw.line(fo_felulet, (0,0,255), (100,100), (200,200), vonal_size)

        for vonal in vonalak:
            if vonal[0] in kivalasztott and vonal[1] in kivalasztott:
                pygame.draw.line(fo_felulet, kivVonal, vonal[0], vonal[1], vonal_size)
            else:
                pygame.draw.line(fo_felulet, norVonal, vonal[0], vonal[1], vonal_size)
            if vonal[0] in kivalasztott:
                pygame.draw.circle(fo_felulet, kivPont, vonal[0], kor_size)
            else:
                pygame.draw.circle(fo_felulet, norPont, vonal[0], kor_size)

            if vonal[1] in kivalasztott:
                pygame.draw.circle(fo_felulet, kivPont, vonal[1], kor_size)
            else:
                pygame.draw.circle(fo_felulet, norPont, vonal[1], kor_size)
            
        ora.tick(30)
        esemeny = pygame.event.get()
        mousePos = pygame.mouse.get_pos()
        mousePosX, mousePosY = mousePos

        shiftDown(esemeny)
        if eventInList(pygame.QUIT, esemeny):
            pygame.quit()
            saveProjekt(infosDict, vonalak)
            exit() 
        elif eventInList(pygame.KEYDOWN, esemeny):
            key = es.dict['key']
            if key == 27:# Az Escape billentyű
                saveProjekt(infosDict, vonalak)
                break
            elif key == ord('s'):# Az 's' gomb megnyomásakor
                pygame.quit()
                saveProjekt(infosDict, vonalak, True)
                break
            elif key == ord('p'):
                TERV = True
                egerAllapot = ''
        elif eventInList(pygame.MOUSEBUTTONDOWN, esemeny):
            if mousePosY > talca_size:
                if egerAllapot == 'lent':
                    vegHely = es.dict['pos']
                    egerAllapot = "fent"
                else:
                    kezdHely = es.dict['pos']
                    egerAllapot = "lent"
                    if TERV and bestTav == -1:
                        TERV = False
                        egerAllapot = ''
                        bestVonal = []
                        kivalasztott = []
                        bestTav = -2
        if TERV:
            tmp = False
            if egerAllapot == 'lent':
                for vonal in vonalak:
                    tav = tavolsag(kezdHely,vonal[0])
                    if tav < kor_size:
                        kezdHely = vonal[0]
                        tmp = True
                    tav = tavolsag(kezdHely,vonal[1])
                    if tav < kor_size:
                        kezdHely = vonal[1]
                        tmp = True
                
                if kezdHely not in kivalasztott and tmp:
                    kivalasztott.append(kezdHely)
            elif egerAllapot == 'fent':
                if bestTav != -1:
                    tmp = False
                    for vonal in vonalak:
                        tav = tavolsag(vegHely, vonal[0])
                        if tav < kor_size:
                            vegHely = vonal[0]
                            tmp = True
                        tav = tavolsag(vegHely, vonal[1])
                        if tav < kor_size:
                            vegHely = vonal[1]
                            tmp = True
                    if tmp:
                        plan(kezdHely, vegHely, megtettHelyek=[])
                        for j in bestVonal:
                            if j.poz not in kivalasztott:
                                kivalasztott.append(j.poz)
                        #bestTav = -1
                        print('A legjobb útvonal kiszámítva!')
                        print('Tav: ' + str(bestTav))
                        bestTav = -1
        elif egerAllapot == "lent":
            #A kattintott helyet igazítja egy meglévő ponthoz
            for vonal in vonalak:
                tav = tavolsag(kezdHely,vonal[0])
                if tav < kor_size:
                    kezdHely = vonal[0]
                tav = tavolsag(kezdHely,vonal[1])
                if tav < kor_size:
                    kezdHely = vonal[1]
                
            
            poz = pygame.mouse.get_pos()
            if shift:
                x1, y1 = kezdHely
                x2, y2 = poz
                if abs(abs(x1 - x2) - abs(y1 - y2)) < abs(y1 - y2) and abs(abs(x1 - x2) - abs(y1 - y2)) < abs(x1 - x2):
                    x2 -= x1
                    y2 -= y1
                    tmpX = x2/abs(x2)# Vagy 1 vagy -1
                    tmpY = y2/abs(y2)# Vagy 1 vagy -1
                    x2 = abs(x2)
                    y2 = abs(y2)
                    x2, y2 = (x2 + y2)/2, (x2 + y2)/2
                    x2, y2 = x2 * tmpX, y2 * tmpY
                    poz = x2 + x1, y2 + y1
                elif abs(x1 - x2) < abs(y1 - y2):#Az Y-on egyenes
                    poz = (x1, y2)
                elif abs(x1 - x2) > abs(y1 - y2):#Az X-en egyenes
                    poz = (x2, y1)
            else:
                #A még nem lehelyezett végpontot igazítja
                for vonal in vonalak:
                    tav = tavolsag(poz,vonal[0])
                    if tav < kor_size:
                        poz = vonal[0]
                    tav = tavolsag(poz,vonal[1])
                    if tav < kor_size:
                        poz = vonal[1]
            
            pygame.draw.line(fo_felulet,(0,0,255),kezdHely,poz,vonal_size)
        elif egerAllapot == "fent":
            if not shift:
                for vonal in vonalak:
                    tav = tavolsag(vegHely,vonal[0])
                    if tav < kor_size:
                        vegHely = vonal[0]
                    tav = tavolsag(vegHely,vonal[1])
                    if tav < kor_size:
                        vegHely = vonal[1]
                vonalak.append([kezdHely,vegHely])
            else:
                vegHely = poz
                vonalak.append([kezdHely,poz])
            egerAllapot = ''
            Pont(kezdHely).new2(Pont(vegHely).hely)
        
        pygame.draw.rect(fo_felulet, Color.grey, pygame.Rect(0, 0, felulet_meret_x, talca_size))
        drawAllFejlecBlokk(fo_felulet)
        if button_undo.draw(fo_felulet):
            vonalak = Undo(vonalak)
        if button_save.draw(fo_felulet):
            print('SAVE Start')
            print(infosDict, vonalak, True, openedFileName)
            saveProjekt(infosDict, vonalak, True, openedFileName)
            print('SAVE End')
        if button_open.draw(fo_felulet):
            tmp = openFile(path)
            if tmp == None:
                main()
            else:
                tmp, openedFileName = tmp
                infosDict, txt = tmp
                main(infosDict, txt, openedFileName)
            pygame.quit()
            main(infosDict, txt)
        if button_settings.draw(fo_felulet):
            mode_setings = not mode_setings
        if mode_setings:
            event_settings(fo_felulet, button_settings, talca_size)
        pygame.display.flip()
    pygame.quit()




bemutat = '''
Ebben a programban terveket / rajzokat tudsz készíteni kattintásokkal.
 - A "SHIFT" nyomásával szabályos függőleges, vízszintes vagy átlós vonalat tudsz rajzolni.
   (Az egérmutató helyétől függően.)
 - Az "S" gomb lenyomásával elmentheted a programodat egy névre.
 - Kilépni az "ESCAPE" gombbal vagy az ablak normál bezárásával tudsz.
   Ilyenkor a gép egyből elmenti a tervet egy adott névre (eredetileg "elozoRajz"-ra).
 - A "P" gomb lenyomásával tudsz "útvonalakat tervezni". Ilyenkor válassz ki két pontot
   és a gép megkeresi a legrövidebb útvonalat.
Indításkor (betöltéskor) az "ENTER" megnyomásával üres tervet hozol létre,
de a felsorolt nevekből importálhatsz is.
'''

'''tmp = openFile(path)
if tmp == None:
    main()
else:
    tmp, openedFileName = tmp
    infosDict, txt = tmp
    main(infosDict, txt, openedFileName)'''
main()
