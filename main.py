import pygame
import compatibility_checker

from path import *
from settings import *
from surface_events import *
from projekt_manager import *
from file_manager import *
from plan_mode import *
from map_writer import *
from the_algorihm import *

ora = pygame.time.Clock()
shift = False
openedFileName = None

pygame.font.init()
myfont = pygame.font.SysFont('Calibri', 30)

def main(dict = {}, v = [], openedFileName = None):
    pygame.init()
    X1, Y1 = SCREEN_SIZE
    tmpX, tmpY = Default.MONITOR_MODE
    felulet_meret_x = X1 + tmpX
    felulet_meret_y = Y1 + tmpY
    del tmpX
    del tmpY

    fo_felulet = pygame.display.set_mode((felulet_meret_x,felulet_meret_y))
    if openedFileName == None:
        pygame.display.set_caption('Roads')
    else:
        pygame.display.set_caption('Roads - ' + openedFileName)
    pygame.display.set_icon(window_icon)
    icon_size = (Default.TALCA_SIZE-15, Default.TALCA_SIZE-15)
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
    mode_setings = False
    '''global bestTav
    global bestVonal'''

    if v != []:
        load_vonalak(vonalak)

    while True:
        global bestVonal
        fo_felulet.fill(Default.HATTER)
        pygame.draw.line(fo_felulet, (0,0,255), (100,100), (200,200), Default.VONAL_SIZE)

        for vonal in vonalak:
            if vonal[0] in kivalasztott and vonal[1] in kivalasztott:
                pygame.draw.line(fo_felulet, Default.KIV_VONAL, vonal[0], vonal[1], Default.VONAL_SIZE)
            else:
                pygame.draw.line(fo_felulet, Default.NOR_VONAL, vonal[0], vonal[1], Default.VONAL_SIZE)
            
            for i in range(2):#0 és 1
                if vonal[i] in kivalasztott:
                    pygame.draw.circle(fo_felulet, Default.KIV_PONT, vonal[i], Default.KOR_SIZE)
                else:
                    pygame.draw.circle(fo_felulet, Default.NOR_PONT, vonal[i], Default.KOR_SIZE)

            
        ora.tick(30)
        esemenyek = pygame.event.get()
        mousePos = pygame.mouse.get_pos()
        mousePosX, mousePosY = mousePos

        # Gombok kezelése
        shiftDown(esemenyek)
        for event in esemenyek:
            if event.type == pygame.QUIT:
                pygame.quit()
                saveProjekt(infosDict, vonalak)
                exit()
            elif event.type == pygame.KEYDOWN:
                key = int(event.dict['key'])
                print(key, type(key))
                if key == 27:# Az Escape billentyű
                    saveProjekt(infosDict, vonalak)
                    exit()
                elif key == ord('s'):# Az 's' gomb megnyomásakor
                    pygame.quit()
                    saveProjekt(infosDict, vonalak, True)
                    break
                elif key == ord('p'):
                    TERV = True
                    egerAllapot = ''
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.dict['pos']
                if mousePosY > Default.TALCA_SIZE:
                    if egerAllapot == 'lent':
                        vegHely = pos
                        egerAllapot = "fent"
                    else:
                        kezdHely = pos
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
                    if tav < Default.KOR_SIZE:
                        kezdHely = vonal[0]
                        tmp = True
                    tav = tavolsag(kezdHely,vonal[1])
                    if tav < Default.KOR_SIZE:
                        kezdHely = vonal[1]
                        tmp = True
                
                if kezdHely not in kivalasztott and tmp:
                    kivalasztott.append(kezdHely)
            elif egerAllapot == 'fent':
                if bestTav != -1:
                    tmp = False
                    for vonal in vonalak:
                        tav = tavolsag(vegHely, vonal[0])
                        if tav < Default.KOR_SIZE:
                            vegHely = vonal[0]
                            tmp = True
                        tav = tavolsag(vegHely, vonal[1])
                        if tav < Default.KOR_SIZE:
                            vegHely = vonal[1]
                            tmp = True
                    if tmp:
                        bestTav, bestVonal = plan(kezdHely, vegHely, megtettHelyek=[])
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
                if tav < Default.KOR_SIZE:
                    kezdHely = vonal[0]
                tav = tavolsag(kezdHely,vonal[1])
                if tav < Default.KOR_SIZE:
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
                    if tav < Default.KOR_SIZE:
                        poz = vonal[0]
                    tav = tavolsag(poz,vonal[1])
                    if tav < Default.KOR_SIZE:
                        poz = vonal[1]
            
            pygame.draw.line(fo_felulet,(0,0,255),kezdHely,poz,Default.VONAL_SIZE)
        elif egerAllapot == "fent":
            if not shift:
                for vonal in vonalak:
                    tav = tavolsag(vegHely,vonal[0])
                    if tav < Default.KOR_SIZE:
                        vegHely = vonal[0]
                    tav = tavolsag(vegHely,vonal[1])
                    if tav < Default.KOR_SIZE:
                        vegHely = vonal[1]
                vonalak.append([kezdHely,vegHely])
            else:
                vegHely = poz
                vonalak.append([kezdHely,poz])
            egerAllapot = ''
            Pont(kezdHely).new2(Pont(vegHely).hely)
        

        pygame.draw.rect(fo_felulet, Color.grey, pygame.Rect(0, 0, felulet_meret_x, Default.TALCA_SIZE))
        drawAllFejlecBlokk(fo_felulet)
        
        # Gombok a tálcán
        if button_undo.draw(fo_felulet):
            vonalak = Undo(vonalak)

        if button_save.draw(fo_felulet):
            saveProjekt(infosDict, vonalak, True, openedFileName)

        if button_open.draw(fo_felulet):
            tmp = openFile(SAVE_PATH)
            #pygame.display.set_mode()
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
            event_settings(fo_felulet, button_settings, Default.TALCA_SIZE)
        
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

main()