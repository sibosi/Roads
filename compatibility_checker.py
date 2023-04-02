import sys
from time import sleep

version = sys.version.split(' ')[0].split('.')
version = version[0] + '.' + version[1]
print('Python version: ' + version)

if version == '3.11':
    print('\n!!!WARNING!!!\nThis Python version (3.11) is not supported!\nUse the Python 3.10 to running!')
    sleep(5)
    exit()
