"Generate structured image"
from pathlib import Path
#from math import cos, sin, pi
from PIL import Image
from statistics import mean
from matplotlib import pyplot as plt
import scipy.signal
import numpy as np

_DEBUG = False

def analyze_picture(pic):
    "print information about image"
    img = Image.open(pic)
    gray = img.convert('L')
    print("Color")
    print(f"Image size: {img.width}x{img.height}")
    print("Image bands", img.getbands())
    print("Image extrema:", img.getextrema())
    print("Gray Image extrema:", gray.getextrema())
    
    histogram = img.histogram()
    #print("histogram", histogram)
    center = img.width // 2
    m_list = []
    for y in range(img.height):
        m_list.append(gray.getpixel((center, y)))
    #print(m_list)
    print('Min:', min(m_list), "Max", max(m_list), "Mean", mean(m_list))
    plt.plot(m_list)
    b, a = scipy.signal.butter(3, [0.01, 0.05],'band')
    # filtered = scipy.signal.lfilter(b, a, m_list)
    # plt.plot(filtered)
    plt.show()

if __name__ == '__main__':
    folder = Path(__file__).parent / 'data/wand'
    picture = folder / "wand.jpg"
    analyze_picture(picture)
