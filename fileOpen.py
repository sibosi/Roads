from tkinter import *
from tkinter import filedialog
from ctypes import windll
import tkinter
windll.shcore.SetProcessDpiAwareness(1)
root = tkinter.Tk()
photo = tkinter.PhotoImage(file = 'arrow.png')
root.wm_iconphoto(False, photo)
root.withdraw()


def saveFile(path : str, fileText : str, defaultName = None):
    file = filedialog.asksaveasfile(initialdir=path,
                                    initialfile=defaultName,
                                    defaultextension='.txt',
                                    filetypes=[
                                        ("Text file",".txt"),
                                        ("CSV file", ".csv"),
                                        ("All files", ".*"),
                                    ])
    filetext = str(fileText)
    #filetext = input("Enter some text I guess: ") //use this if you want to use console window
    try:
        file.write(filetext)
        file.close()
    except:
        pass


def openOldFile(path, v):
    import os
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
    return (infosDict, txt)


def openFile(path):
    filepath = filedialog.askopenfilename(initialdir=path,
                                          title="Select a txt or a csv file, else click the back",
                                          filetypes= (("text files","*.txt"),
                                          ("all files","*.*")))

    tmp = filepath.split('\\')
    v = tmp.pop(len(tmp)-1)
    v = v.split('.')[0]
    openedFileName = str(filepath).split('/').pop(len(tmp)-1).split('.')[0]
    
    oldPath = ''
    for item in tmp:
        oldPath= oldPath + item + '\\'
    oldPath = oldPath[:-2]

    try:
        tmp = openOldFile(oldPath, v)
    except:
        return None
    return (tmp, openedFileName)

if __name__ == '__main__':
    path = r'C:\Users\sibos\Documents\GitHub\Roads'
    saveFile(path, 'Test')
