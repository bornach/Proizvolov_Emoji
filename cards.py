#!/usr/bin/env python
from __future__ import division, print_function

# test missing card idea using Proizvolov identity

import random, sys

nCards = 11

cardValue = [0, 1, 2, 3, 4, 10, 11, 12, 13, 14, 15]
altValue = [9, 8, 7, 6, 5, 10, 9, 8, 7, 6, 5]

nHalf = (nCards - 1) // 2

def calcProizvolov(cardsA, cardsB):
    cardsA.sort()
    cardsB.sort(reverse=True)
    i = 0
    result = 0
    for x in cardsA:
        y = cardsB[i]
        result += abs(x - y)
        i += 1
    return result

print("Test Proizvolov identity")
checkMod = [0] * nCards
cycle = [0] * nCards
for i in range(nCards):
    cardsA = []
    cardsB = []
    
    chooseA = []
    n = nHalf
    for j in range(nHalf):
        k = random.randint(0,n)
        n -= k
        chooseA.append(k)
        
    for j in range(nCards):
        if i != j:
            if len(chooseA) == 0 or chooseA[0] > 0:
                cardsA.append(cardValue[j])
                if len(chooseA) > 0: chooseA[0] -= 1
            else:
                chooseA = chooseA[1:]
                cardsB.append(cardValue[j])

    p = calcProizvolov(cardsA, cardsB)
    checkMod[i] = p % nCards
    print(i, cardsA, cardsB, p, checkMod[i])
    cycle[checkMod[i]] = i

print("Moves tables")
moves = [[0] * nCards for i in range(nCards)]


print("   ",":".join(["{:2d}".format(x) for x in range(nCards)]))
for i in range(nCards):
    print("{:2d}".format(i), end=":")
    for j in range(nCards):
        moves[i][j] = abs(cardValue[i] - cardValue[j]) % nCards
        if (i > nHalf and j > nHalf) or (i < nHalf and j < nHalf):
            moves[i][j] = abs(cardValue[i] - altValue[j]) % nCards
        print("{:3d}".format(moves[i][j]), end="")
    print()




# generate circle of symbols - a token will be moved clockwise/counter-clockwise on this circle

    
# test transformed actions
print("Transformed")

# verification
fail = 0
for i in range(nCards):
    for trial in range(100):
        cardsA = []
        cardsB = []

        shuffled = range(nCards)
        random.shuffle(shuffled)
        print("shuffled",shuffled)

        mask = [0] * nCards
        j = nHalf
        while j > 0:
            k = random.randint(0, nCards - 1)
            if shuffled[k] != i and mask[k] == 0:
                mask[k] = 1
                j -= 1



        for j in range(nCards):
            if i != shuffled[j]:
                if mask[j] == 1:
                    cardsA.append(shuffled[j])
                else:
                    cardsB.append(shuffled[j])

        position = 0
        for j in range(nHalf):
            position = position + moves[cardsA[j]][cardsB[j]]
        print(i, cardsA, cardsB, position, position % nCards)
        if (position % nCards) != checkMod[i]:
            print("FAILED!")
            fail = 1
if fail:
    sys.exit(1)

## create card images
icons = ["1F33B.png", "1FA82.png", "1F34E.png", "1F41F.png", "1F436.png", "1F603.png", "1F984.png", "1F986.png", "1F347.png", "2665.png", "270F.png"]
icons.reverse()

#icons = ["airplane.png", "owl.png", "butterfly.png", "crab.png", "fox_face.png", "green_apple.png", "grinning_face.png", "key.png", "musical_note.png", "turtle.png", "wrench.png"]


from PIL import Image, ImageDraw, ImageFont
from math import sin, cos, pi

imageSize = (640, 800)
image = Image.new("RGB", imageSize, (255,255,255))

r = imageSize[0] / 3 + 20
x0 = imageSize[0] // 2
y0 = imageSize[1] // 2

iconWidth = 120
iconHeight = 120

mode = 1

r0 = r - 60
r1 = r + 84

draw = ImageDraw.Draw(image)
for i in range(nCards):
    # start position is top most icon
    angle = 2*pi*i/nCards
    iconImage = Image.open(icons[cycle[i]]).convert("RGBA")
    iconResized = iconImage.resize((iconWidth,iconHeight))
    x1 = int(x0 + r*sin(angle))
    y1 = int(y0 - r*cos(angle))
    image.paste(iconResized, (x1  - iconWidth // 2, y1 - iconHeight // 2), mask=iconResized)

    # draw fences between icons
    a0 = 2*pi*(i - 0.5)/nCards
    a1 = 2*pi*(i + 0.5)/nCards


    xy = [(x0 + r0*sin(a0), y0 - r0*cos(a0)), (x0 + r1*sin(a0), y0 - r1*cos(a0)), (x0 + r1*sin(a1), y0 - r1*cos(a1))]

    draw.line(xy, width=3, fill=(0, 0, 0))

#border
draw.rectangle([(1,1),(imageSize[0]-2, imageSize[1]-2)], outline=(80,80,80), width = 2)
image.save("cycle.png")

# generate movement card backs

class CardBack:
    def __init__(self, iconFiles, imageSize, radius):
        self.icons = iconFiles
        self.size = imageSize
        self.iconWidth = 120
        self.iconHeight = 120
        self.r0 = radius - 64
        self.r1 = radius + 36
        self.nCards = len(iconFiles)
        self.mode = 1

    def generate(self, tokenMove, index):
        image = Image.new("RGB", self.size, (255,255,255))
        draw = ImageDraw.Draw(image)

        #border
        draw.rectangle([(1,1),(self.size[0]-2, self.size[1]-2)], outline=(0,0,0), width = 1)
        draw.rectangle([(0,0),(self.size[0]-1, self.size[1]-1)], outline=(120,120,120), width = 1)

        j0 = 0
        nShow = self.nCards - 1
        if self.mode == 1: nShow = self.nCards
        for j in range(nCards):
            if index == j and self.mode == 0: continue

            angle = 2*pi*(j0 - index) / nShow
            iconIndex = j
            if self.mode == 1:
                angle = pi / 2 - (2*pi*j / nShow)
                iconIndex = cycle[j]

            iconImage = Image.open(self.icons[iconIndex]).convert("RGBA")
            iconResized = iconImage.resize((self.iconWidth, self.iconHeight))
            j0 += 1

            x1 = int(x0 + self.r1*cos(angle))
            y1 = int(y0 - self.r1*sin(angle))
            image.paste(iconResized, (x1  - self.iconWidth // 2, y1 - self.iconHeight // 2), mask=iconResized)

            # token movement actions
            
            x1 = int(x0 + self.r0*cos(angle))
            y1 = int(y0 - self.r0*sin(angle))
            move = tokenMove[iconIndex]
            if move > 5 and self.mode == 0: move -= 11
            moveMag = abs(move)
            text = "{}".format(moveMag)
            textWidth, textHeight = font.getsize(text)
            draw.text((x1 - textWidth//2, y1 - textHeight//2 - 4), text, fill = (0,0,0), font=font)

            if self.mode == 1:
                draw.ellipse([(x1-40, y1-40),(x1+40,y1+40)], outline = (0,0,0), width = 2)
            else:
                s = 0
                if move > 0: s = 1
                elif move < 0: s = -1
                # +1 for clockwise
                # -1 for anti-clockwise
                self.arcArrows(draw, x1, y1, 2, s)

        if self.mode == 1:
            self.arcArrows(draw, x0, y0, 5, 1)
        return image

    def arcArrows(self, draw, x, y, f, s):
        colour = (80, 80, 80)
        d = 20 * f
        for d1 in [0, 1]:
            draw.arc([(x-d+d1, y-d),(x+d+d1,y+d)], -60, 60, fill = colour, width = f+1)
            draw.arc([(x-d+d1, y-d),(x+d+d1,y+d)], 120, 240, fill = colour, width = f+1)

        if s != 0:
            x2 = x + 8*f
            y2 = y + 19 * f * s
            xy = [(x2, y2), (x2+8*f, y2-4*f*s), (x2+4*f, y2-8*f*s)]
            draw.polygon(xy, fill = colour, outline = colour)

            x2 = x - 8*f
            y2 = y - 19 * f * s
            xy = [(x2, y2), (x2-8*f, y2+4*f*s), (x2-4*f, y2+8*f*s)]
            draw.polygon(xy, fill = colour, outline = colour)


#iconWidth = 90
#iconHeight = 90
#r1 = r + 36
#r0 = r - 64

frontWidth = imageSize[0] - 120


font = ImageFont.truetype("arialbd.ttf", 50)

for i in range(nCards):
    # back of card
    cardBack = CardBack(icons, imageSize, r)
    cardBack.mode = mode
    image = cardBack.generate(moves[i], i)
    
    image.save("back{:02d}.png".format(i))

    #front of card
    image = Image.new("RGB", imageSize, (255, 255, 255))
    iconImage = Image.open(icons[i]).convert("RGBA")
    iconResized = iconImage.resize((frontWidth, frontWidth), resample=Image.BICUBIC)
    image.paste(iconResized, (x0 - frontWidth // 2, y0 - frontWidth // 2), mask = iconResized)

    draw = ImageDraw.Draw(image)
    
    #border
    draw.rectangle([(1,1),(imageSize[0]-2, imageSize[1]-2)], outline=(0,0,0), width = 1)
    draw.rectangle([(0,0),(imageSize[0]-1, imageSize[1]-1)], outline=(120,120,120), width = 1)
    
    image.save("front{:02d}.png".format(i))

# panelise into 3 large images for printing
margin = 70
for panelIndex in [0, 1, 2]:
    panelWidth = imageSize[1] * 2 + 2*margin
    panelHeight = imageSize[0] * 4 + 2*margin
    panelImage = Image.new("RGB", (panelWidth, panelHeight), (255,255,255))
    for i in range(4):
        j = panelIndex * 4 + i
        if j < 11:
            frontImage = Image.open("front{:02d}.png".format(j))
            backImage = Image.open("back{:02d}.png".format(j))
        elif mode == 0:
            frontImage = Image.open("cycle.png")
            backImage = Image.new("RGB",imageSize, (255,255,255))
        else:
            break

        panelImage.paste(frontImage.rotate(90, expand=1), ((i % 2) * imageSize[1] + margin, (i // 2) * imageSize[0] * 2 + margin))
        panelImage.paste(backImage.rotate(90, expand=1), ((i % 2) * imageSize[1] + margin, ((i // 2) * 2 + 1) * imageSize[0] + margin))

    panelImage.save("shuffle{}.png".format(panelIndex))
