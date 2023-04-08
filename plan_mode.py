import pygame
from settings import *
from the_algorihm import *

#Le van-e nyomva a Shift?
def shiftDown(list, shift = None):
    for element in list:
        if element.type == pygame.KEYDOWN:
            if element.dict['key'] == 1073742053 or element.dict['key'] == 1073742049:
                shift = True
    for element in list:
        if element.type == pygame.KEYUP:
            if element.dict['key'] == 1073742053 or element.dict['key'] == 1073742049:
                shift = False
    return shift

def Plan_On_Map(egerAllapot, vonalak, kivalasztott, bestTav,
                kezdHely, vegHely):
    tmp = False
    bestVonal = []
    if egerAllapot == 'lent':
        for vonal in vonalak:
            tav = tavolsag(kezdHely, vonal[0])
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
            vegHely, tmp = kord_igazitas(vegHely, vonalak)
            if tmp:
                import datetime
                TIME = datetime.datetime.now()
                bestTav, bestVonal = plan(pontok, kezdHely, vegHely)#, pont_ids, megtettHelyek=[]v
                print(datetime.datetime.now() - TIME)
                for j in bestVonal:
                    print(type(bestVonal))
                    if j.poz not in kivalasztott:
                        kivalasztott.append(j.poz)
                #bestTav = -1
                print('A legjobb útvonal kiszámítva!')
                print('Tav: ' + str(bestTav))
                bestTav = -1
    return (egerAllapot, vonalak, kivalasztott, bestTav, bestVonal, kezdHely, vegHely)