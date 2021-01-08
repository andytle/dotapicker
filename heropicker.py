from PIL import Image
import os
import numpy as np
# creating an image object 

# while True:
#     im = ImageGrab.grab()
#     dt = datetime.now()
#     fname = "pic_{}.{}.png".format(dt.strftime("%H%M_%S"), dt.microsecond // 100000)
#     im.save(fname, 'png') 

# heroes = []

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
    img.show()
    # cutoff = 15 
    # hash0 = imagehash.average_hash(img)
    img = np.atleast_3d(img)

    for hero in os.listdir("./heroes"):
        hero_img = Image.open("./heroes/" + hero) 
    
        hero_img = np.atleast_3d(hero_img)
        H, W, D = hero_img.shape[:3]
        h, w = img.shape[:2]

        # Integral image and template sum per channel
        sat = img.cumsum(1).cumsum(0)
        hero_imgsum = np.array([hero_img[:, :, i].sum() for i in range(D)])

        # Calculate lookup table for all the possible windows
        iA, iB, iC, iD = sat[:-h, :-w], sat[:-h, w:], sat[h:, :-w], sat[h:, w:] 
        lookup = iD - iB - iC + iA
        # Possible matches
        possible_match = np.where(np.logical_and.reduce([lookup[..., i] == hero_imgsum[i] for i in range(D)]))

        # Find exact match
        for y, x in zip(*possible_match):
            if np.all(img[y+1:y+h+1, x+1:x+w+1] == hero_img):
                return hero

    return None

if __name__ == "__main__":
    img = getTopBar("8le3puzyk45y.png")
    heroPortraits = getHeroPortraits(img)
    radiant = heroPortraits[0:5]
    dire = heroPortraits[-5:]
    matchHero(dire[3])
    # for heroPortrait in dire:
    #     heroPortrait.show()
