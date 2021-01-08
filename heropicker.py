from PIL import Image, ImageGrab
import os
import numpy as np
import cv2
import datetime

def printScreen():
    im = ImageGrab.grab()
    fname = "pic_{}.{}.png")
    im.save(fname, 'png') 


def getTopBar(img_path):
    img_orig = Image.open(img_path) 
    width, height = img_orig.size
    crop_size = (0, 0, width, height/10)
    img = img_orig.crop(crop_size)
    return img

def getIntervals(img):
    intervals = []
    img = img.convert('RGB')
    # r_target, g_target, b_target = (22,31,39)
    r_target, g_target, b_target = (109, 125, 142)
    offset = 20
    portraitSpaceOffset = 20
    begin = -1
    end = begin

    pixels = img.load() # create the pixel map
    textTopLine = -1
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            r, g, b = pixels[i,j]
            if r in range(r_target-offset, r_target+offset) and g in range(g_target-offset, g_target+offset) and b in range(b_target-offset, b_target+offset):
                # pixels[i,j] = (255,255,255)
                textTopLine = max(textTopLine, j)
                if begin == -1:
                    begin = i
                    end = i

                if i - end < portraitSpaceOffset:
                    end = i
                else:
                    intervals.append((begin, end))
                    begin = -1

                break    

    return intervals, textTopLine

def outline(img, intervals, portrait_bottom):
    pixels = img.load() # create the pixel map
    for interval in intervals:
        for j in range(img.size[1]):
            (begin, end) = interval
            pixels[begin,j] = (0,0,0)
            pixels[end,j] = (0,0,0)

    
    for i in range(img.size[0]):
        pixels[i, portrait_bottom] = (0,0,0)
    img.show()


def getHeroPortraits(img, show_detect = False):
    heroPortraits = []
    intervals, textTopLine = getIntervals(img)
    FROM_BOTTOM_TEXT_TO_PORTRAIT_BOTTOM = 22

    portrait_bottom = textTopLine - FROM_BOTTOM_TEXT_TO_PORTRAIT_BOTTOM
    for interval in intervals:
        (begin, end) = interval

        crop_size = (begin, 0, end, portrait_bottom)
        heroPortraits.append(img.crop(crop_size))

    if show_detect:
        outline(img,intervals,portrait_bottom)
    
    print(intervals)

    return heroPortraits

def matchHero(img):
    width, height = img.size
    crop_size = (width/4, height/4, 3*width/4, 3*height/4)
    img = img.crop(crop_size)
    # for hero in os.listdir("./heroes"):
            

if __name__ == "__main__":
    # printScreen()
    img = getTopBar("8le3puzyk45y.png")
    heroPortraits = getHeroPortraits(img)
    radiant = heroPortraits[0:5]
    dire = heroPortraits[-5:]
    matchHero(dire[3])
    # for heroPortrait in dire:
    #     heroPortrait.show()
