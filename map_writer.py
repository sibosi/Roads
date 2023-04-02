from datetime import datetime
from path import *
from file_manager import *


# Térképleíró és file-ba író
def saveProjekt(infosDict, vonalak, name = False, openedFileName = None):
    if not name:
        file = open(os.path.expanduser(os.path.join(SAVE_PATH, 'elozoRajz' + '.txt')), 'w')
    #os.path.expanduser(os.path.join("~/Desktop",boyka + ".txt"))
    
    # A térkép leírója TXT-be
    tmp = ''
    for ket_pont in vonalak:
        for pont_kord in ket_pont:
            tx, ty = pont_kord
            tmp = tmp+str(tx)+' '+str(ty)+','
        tmp = tmp[:len(tmp)-1]
        tmp = tmp+'/'
    tmp = tmp[:len(tmp)-1]

    # Dátum címkézése
    infosDict['created'] = str(datetime.now())
    infos = ''
    for key, value in infosDict.items():
        infos = infos + key + ':' + value + '\n'

    # Összefűzés, majd file-ba írás
    tmp = infos + tmp
    if not name:
        file.write(tmp)
    file = open(os.path.expanduser(os.path.join(SAVE_PATH, 'e' + '.txt')), 'w')
    file.write(tmp)
    file.close()

    if name:
        saveFile(SAVE_PATH, tmp)
