from pathlib import Path
import os

KONYVTAR = 'Roads tervek'

#file inportálása:
SAVE_PATH = Path(__file__).parent / KONYVTAR #mentési hely elérési útja
if not os.path.exists(SAVE_PATH):# ha nincs ilyen mappa, akkor készít egyet
    os.makedirs(SAVE_PATH)

#actual path
ROOT_PATH = Path(__file__).parent
IMAGE_PATH = ROOT_PATH / 'Images'
