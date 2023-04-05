"Calculate dias position"
from pathlib import Path
from math import tan
from PIL import Image

INCH = 2.54

GRAD_PR_PERIOD = 1.29   # degree

DIAS_FREQ = 41   # pixels pr period

_DEBUG = True

def picture_size(imgfile):
    "get the physical size of picture"
    img = Image.open(imgfile)
    # img.load()
    dpi = img.info.get('dpi', None)
    if dpi:
        size = (img.width/dpi[0]*INCH, img.height/dpi[1]*INCH)
    else:
        size = None
    if _DEBUG:
        exif = img.getexif()
        print("Exif", exif)
        print(img.format, img.size, img.mode)
        print("dpi", dpi)
    return size

def calculate_position(picture):
    sz = picture_size(picture)
    print(sz)
    img = Image.open(picture)
    period_size = DIAS_FREQ / img.height * sz[0]
    print(f"Period size {period_size} mm")

    l = period_size / tan(GRAD_PR_PERIOD)
    print(f"Length {l} mm")
    return


if __name__ == '__main__':
    picture = Path(__file__).parent / 'data/greyA.png'

    sz = picture_size(picture)
    print("Size (mm)", sz)
    calculate_position(picture)


