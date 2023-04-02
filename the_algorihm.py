from settings import *
from projekt_manager import *

loading = 0
bestTav = -2
bestVonal = []
def plan(poz1, poz2, tav=0, megtettHelyek = [],
         loading = loading, bestTav = bestTav, bestVonal = bestVonal):
    item = pont_ids[poz1]
    win = pont_ids[poz2]

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
                    plan(k.poz, poz2, tav, megtettHelyek[:], loading, bestTav, bestVonal)
    return (bestTav, bestVonal)
