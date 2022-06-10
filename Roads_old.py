from datetime import datetime
import os
import pathlib
from time import sleep
import pygame
from math import sqrt
import ctypes#A képernyő nagyságát adja meg

ora = pygame.time.Clock()
konyvtar = 'Roads tervek'
shift = False
OpenedFile = None

#file inportálása:
path = str(str(pathlib.Path(__file__).parent.resolve())+('\{0}'.format(konyvtar)))
newpath = r''+ path# megadja az aktuális mappa elérési útját
if not os.path.exists(newpath):# ha nincs ilyen mappa, akkor készít egyet
    os.makedirs(newpath)

#font
pygame.font.init()
myfont = pygame.font.SysFont('Calibri', 30)

#colors:
red = (255, 0, 0)
green = (0, 255, 8)
blue = (0, 0, 255)
cian = (0, 255, 255)
yellow = (255, 255, 0)
pink = (255, 0, 255)
kiwi = (161, 245, 66)
grey = (241, 241, 241)

kivVonal = kiwi
norVonal = blue
kivPont = cian
norPont = red

#monitorMode:
big = -20, -100
normal = -50, -125
small = -1000, -100
half = -700, -100

monitorMode = normal

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

def mappaTartalma(path = path):
    print('A te tervjeid:')
    names = ['Name']
    namesValueLen = [0]
    mappaLista = listTxtFiles(path)#Az aktuális mappában lévő összes elem.
    
    #A file-ok neveinek a hosszúságát határozzuk meg ([0])
    for name in mappaLista:
        if len(name) > namesValueLen[0]:
            namesValueLen[0] = len(name)

    #Összeszedjük az összes nevet és az értékének a hosszát
    for file in mappaLista:
        file = open(os.path.expanduser(os.path.join(path, file)), 'r')
        infos = file.read().split('\n')[:-1]
        for info in infos:
            info = info.split(':')
            if info[0] not in names:
                names.append(info[0])
                namesValueLen.append(len(info[1]))
            elif namesValueLen[names.index(info[0])] < len(info[1]):
                namesValueLen[names.index(info[0])] = len(info[1])
        file.close()
    
    #Fejléc elkészítés
    infosD = makeDict(names, namesValueLen)
    i = 0
    for name in names:
        j = infosD[name] - len(name)
        print(name + ' '* (j + 3), end = '')
        i += 1
    print()

    TMP = names, namesValueLen
    for elem in mappaLista:
        names, namesValueLen = TMP
        file = open(os.path.expanduser(os.path.join(path, elem)), 'r')
        infos = file.read().split('\n')[:-1]
        print(elem + (namesValueLen[0] - len(elem)) * ' ', end='   ')
        names = names[1:]
        namesValueLen = namesValueLen[1:]
        for name in names:
            tmp = True
            for info in infos:
                info = info.split(':')
                if info[0] == name:
                    print(info[1] + (infosD[name] - len(info[1])) * '-', end='   ')
                    tmp = False
            if tmp:
                print(infosD[name] * '*', end='   ')

        print()
    print()

def tavolsag(a,b):
    x1, y1 = a
    x2, y2 = b
    tav = sqrt((x2-x1)**2+(y2-y1)**2)
    print(f'{a} {b} = {tav}')
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

def saveProjekt(infosDict, vonalak, name = False):
    if name:
        TMP = input('Milyen névre mentenéd a tervet: ')
        if TMP == '':
            TMP = OpenedFile
        file = open(os.path.expanduser(os.path.join(path, TMP +'.txt')), 'w')
    else:
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
    file.write(tmp)
    file = open(os.path.expanduser(os.path.join(path, 'e' + '.txt')), 'w')
    file.write(tmp)

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
    def __init__(self, x, y, image, size=1):
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
                    print(tav)
                    plan(k.poz, poz2, tav, megtettHelyek[:])

def main(dict = {}, v = []):
    pygame.init()
    X1, Y1 = monitorSize()
    tmpX, tmpY = monitorMode
    felulet_meret_x = X1 + tmpX
    felulet_meret_y = Y1 + tmpY
    del tmpX
    del tmpY

    window_icon = pygame.image.load('arrow.png')
    image_undo = pygame.image.load('undo.png')#.convert_alpha()
    image_save = pygame.image.load('save.png')

    fo_felulet = pygame.display.set_mode((felulet_meret_x,felulet_meret_y))
    pygame.display.set_caption('Roads')
    pygame.display.set_icon(window_icon)
    tray_y = 50
    icon_size = (35, 35)
    button_undo = Button(20, 10, image_undo, icon_size)
    button_save = Button(70, 10, image_save, icon_size)

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
        fo_felulet.fill((63,152,107))
        pygame.draw.line(fo_felulet,(0,0,255),(100,100),(200,200),1)

        for vonal in vonalak:
            if vonal[0] in kivalasztott and vonal[1] in kivalasztott:
                pygame.draw.line(fo_felulet,kivVonal,vonal[0],vonal[1],1)
            else:
                pygame.draw.line(fo_felulet,norVonal,vonal[0],vonal[1],1)
            if vonal[0] in kivalasztott:
                pygame.draw.circle(fo_felulet,kivPont,vonal[0],10)
            else:
                pygame.draw.circle(fo_felulet,norPont,vonal[0],10)

            if vonal[1] in kivalasztott:
                pygame.draw.circle(fo_felulet,kivPont,vonal[1],10)
            else:
                pygame.draw.circle(fo_felulet,norPont,vonal[1],10)
            
        ora.tick(30)
        esemeny = pygame.event.get()
        mousePos = pygame.mouse.get_pos()
        mousePosX, mousePosY = mousePos

        shiftDown(esemeny)
        if eventInList(pygame.QUIT, esemeny):
            pygame.quit()
            saveProjekt(infosDict, vonalak)
            break
        elif eventInList(pygame.KEYDOWN, esemeny):
            key = es.dict['key']
            if key == 27:# Az Escape billentyű
                saveProjekt(infosDict, vonalak)
                break
            elif key == ord('s'):# Az 's' gomb megnyomásakor
                pygame.quit()
                mappaTartalma()
                saveProjekt(infosDict, vonalak, True)
                break
            elif key == ord('p'):
                TERV = True
                egerAllapot = ''
        elif eventInList(pygame.MOUSEBUTTONDOWN, esemeny):
            if mousePosY > tray_y:
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
                    if tav < 10:
                        kezdHely = vonal[0]
                        tmp = True
                    tav = tavolsag(kezdHely,vonal[1])
                    if tav < 10:
                        kezdHely = vonal[1]
                        tmp = True
                
                if kezdHely not in kivalasztott and tmp:
                    print('UGANDA:', kezdHely)
                    kivalasztott.append(kezdHely)
            elif egerAllapot == 'fent':
                if bestTav != -1:
                    print(ids.keys)
                    tmp = False
                    for vonal in vonalak:
                        tav = tavolsag(vegHely, vonal[0])
                        if tav < 10:
                            vegHely = vonal[0]
                            tmp = True
                        tav = tavolsag(vegHely, vonal[1])
                        if tav < 10:
                            vegHely = vonal[1]
                            tmp = True
                    if tmp:
                        plan(kezdHely, vegHely, megtettHelyek=[])
                        print('LEN:', len(bestVonal))
                        for j in bestVonal:
                            print('J:', j.poz)
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
                if tav < 10:
                    kezdHely = vonal[0]
                tav = tavolsag(kezdHely,vonal[1])
                if tav < 10:
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
                    if tav < 10:
                        poz = vonal[0]
                    tav = tavolsag(poz,vonal[1])
                    if tav < 10:
                        poz = vonal[1]
            
            pygame.draw.line(fo_felulet,(0,0,255),kezdHely,poz,1)
        elif egerAllapot == "fent":
            if not shift:
                for vonal in vonalak:
                    tav = tavolsag(vegHely,vonal[0])
                    if tav < 10:
                        vegHely = vonal[0]
                    tav = tavolsag(vegHely,vonal[1])
                    if tav < 10:
                        vegHely = vonal[1]
                vonalak.append([kezdHely,vegHely])
            else:
                vegHely = poz
                vonalak.append([kezdHely,poz])
            egerAllapot = ''
            Pont(kezdHely).new2(Pont(vegHely).hely)
        
        
        pygame.draw.rect(fo_felulet, grey, pygame.Rect(0, 0, felulet_meret_x, tray_y))
        if button_undo.draw(fo_felulet):
            vonalak = Undo(vonalak)
        if button_save.draw(fo_felulet):
            pygame.quit()
            mappaTartalma()
            saveProjekt(infosDict, vonalak, True)
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

v = None
while v == 'HELP' or v == None:
    mappaTartalma()
    print('A segítségért írd be "HELP"!')
    v = input('Add meg az egyik terv nevét (vagy nyomj entert): ')
    if v == 'HELP':
        print(bemutat)
        input('Nyomj entert!')
        print('\n')
if v == '':
    main()
else:
    OpenedFile = v
    txt = open(os.path.expanduser(os.path.join(path,v+'.txt')), 'r')
    txt = txt.read()
    infos = txt.split('\n')
    tmp = infos.pop(len(infos)-1).split('/')

    infosDict = {}
    for element in infos:
        element = element.split(':')
        tmpDict = {
            element[0] : element[1]
        }
        infosDict.update(tmpDict)

    txt = []
    for i in tmp:
        txt.append(i.split(','))
    tmp = txt[:]
    for i in tmp:
        for j in i:
            jElozo = j
            j = j.split(' ')
            txt[(txt.index(i))][i.index(jElozo)] = ((int(j[0]), int(j[1])))
    del tmp
    main(infosDict, txt)
