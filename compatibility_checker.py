import sys
from time import sleep

version = sys.version.split(' ')[0].split('.')
version = version[0] + '.' + version[1]
print('Python version: ' + version)

if version == '3.11':
    print('\n!!!WARNING!!!\n\
          This Python version (3.11) is not supported!\n\
          Use the Python 3.10 to running!')
    sleep(5)
    exit()
