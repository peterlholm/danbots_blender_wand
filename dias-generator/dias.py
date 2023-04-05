"Generate structured image"
from pathlib import Path
from math import cos, sin, pi
from PIL import Image
#from PIL.ExifTags import TAGS
from PIL.PngImagePlugin import PngInfo

XPAUTHOR = 40094
XPTITLE = 40092
IMAGEDESCRIPTION = 0x010e

PICTURE_SIZE = 400
HIGH_PERCENT = 12/16.5      # procent of picture with stripes
FREQ = 11                  # number of periods in visiple area
PIC_PR_PERIOD = PICTURE_SIZE * HIGH_PERCENT / FREQ

AMPLITUDE = (155-95)/256.0    #
ZEROPOINT = 120/256.0         # middle of sinus
PIXEL_COLOR = (0, 255, 0)
DPI = 2400
DPIXY = (DPI, DPI)
INCH = 25.4     # mm
_DEBUG = False


def create_dias(folder):
    "create the dias"
    grey = Image.new('L', (PICTURE_SIZE, PICTURE_SIZE))
    greya = Image.new('LA', (PICTURE_SIZE, PICTURE_SIZE),color=(0,255))
    rgb = Image.new('RGB', (PICTURE_SIZE, PICTURE_SIZE))
    rgba = Image.new('RGBA', (PICTURE_SIZE, PICTURE_SIZE))
    print("Picture size: ",PICTURE_SIZE)
    print("Freq (pic/period", PIC_PR_PERIOD)
    print("MM pr periode", PIC_PR_PERIOD/DPI*INCH)
    y_start = int(PICTURE_SIZE*(1-HIGH_PERCENT)/2)
    y_end = PICTURE_SIZE-y_start
    print("Y start/slut", y_start, y_end)
    for y in range(y_start, y_end):
        sval = (y-y_start) / PIC_PR_PERIOD * 2.0 * pi
        intens = -cos(sval)
        val = int((ZEROPOINT + AMPLITUDE*intens)*256)
        #print(y,intens, val)
        #print(val, intens)
        for x in range(PICTURE_SIZE):
            #val = 128 + int(intens * 128)
            grey.putpixel((x, y), val)
            greya.putpixel((x, y), (0, val))
            color = (0, int((1-intens) * 128), 0)
            rgb.putpixel((x, y), color)
            rgba.putpixel((x, y), (0, 255, 0, val))
    savefolder = Path(folder)

    metadata = PngInfo()
    metadata.add_text(
        "Description", f"Freq (pic/period {PIC_PR_PERIOD} mm pr periode {PIC_PR_PERIOD/DPI*INCH}")
    metadata.add_text("Author", "Peter Holm")
    exif = rgb.getexif()
    exif[XPAUTHOR] = "Peter Holm"
    exif[XPTITLE] = f"Freq (pic/period {PIC_PR_PERIOD} mm pr periode {PIC_PR_PERIOD/DPI*INCH}"

    exif[IMAGEDESCRIPTION] = f"Freq (pic/period {PIC_PR_PERIOD} mm pr periode {PIC_PR_PERIOD/DPI*INCH}"

    rgb.save(savefolder / "rgb.png", dpi=DPIXY, exif=exif, pnginfo=metadata)
    rgba.save(savefolder / "rgba.png", dpi=DPIXY, pnginfo=metadata)
    grey.save(savefolder / "grey.png", dpi=DPIXY, pnginfo=metadata)
    greya.save(savefolder / "greyA.png", dpi=DPIXY, pnginfo=metadata)
    # img.save("int.png","I")
    rgb.save(savefolder / "rbg.jpg", dpi=DPIXY, exif=exif, pnginfo=metadata)
    return rgb


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


if __name__ == '__main__':
    folder = Path(__file__).parent / 'data'
    create_dias(folder)
    sz = picture_size(folder / 'rgb.png')
    print("Size (mm)", sz)
