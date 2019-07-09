#!/usr/bin/env python
from __future__ import division, print_function

# test missing card idea using Proizvolov identity

import random

nCards = 11

cardValue = [0, 1, 2, 3, 4, 10, 11, 12, 13, 14, 15]

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
    print(i, cardsA, cardsB, p, (p % nCards))

print("Moves tables")
moves = [[0] * nCards for i in range(nCards)]

for i in range(nCards):
    for j in range(nCards):
        moves[i][j] = abs(cardValue[i] - cardValue[j]) % nCards

    print(i, moves[i])


# generate circle of symbols - a token will be moved clockwise/counter-clockwise on this circle

cycle = [0] * nCards
    
# test transformed actions
print("Transformed"        )
for i in range(nCards):
    cardsA = []
    cardsB = []
    
    
    mask = [0] * nCards
    j = nHalf
    while j > 0:
        k = random.randint(0, nCards - 1)
        if k != i and mask[k] == 0:
            mask[k] = 1
            j -= 1
        
    for j in range(nCards):
        if i != j:
            if mask[j] == 1:
                cardsA.append(j)
            else:
                cardsB.append(j)

    position = 0
    for j in range(nHalf):
        position = (position + moves[cardsA[j]][cardsB[nHalf - 1 - j]]) % nCards
    print(i, cardsA, cardsB, position)
    cycle[position] = i

icons = ["airplane.png", "owl.png", "butterfly.png", "crab.png",
         "fox_face.png", "green_apple.png", "grinning_face.png",
         "key.png", "musical_note.png", "turtle.png", "wrench.png"]


from PIL import Image, ImageDraw, ImageFont
from math import sin, cos, pi

imageSize = (640, 800)
image = Image.new("RGB", imageSize, (255,255,255))

r = imageSize[0] / 3 + 20
x0 = imageSize[0] // 2
y0 = imageSize[1] // 2

iconWidth = 100
iconHeight = 100


r0 = r - 60
r1 = r + 84

draw = ImageDraw.Draw(image)
for i in range(nCards):
    # start position is top most icon
    angle = 2*pi*i/nCards
    iconImage = Image.open(icons[cycle[i]])
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

iconWidth = 90
iconHeight = 90
r1 = r + 36
r0 = r - 64

frontWidth = imageSize[0] - 120


font = ImageFont.truetype("arialbd.ttf", 50)

for i in range(nCards):
    # back of card
    image = Image.new("RGB", imageSize, (255,255,255))
    draw = ImageDraw.Draw(image)
    
    #border
    draw.rectangle([(1,1),(imageSize[0]-2, imageSize[1]-2)], outline=(0,0,0), width = 1)
    draw.rectangle([(0,0),(imageSize[0]-1, imageSize[1]-1)], outline=(120,120,120), width = 1)
    
    j0 = 0
    for j in range(nCards):
        if i == j: continue
        angle = 2*pi*(j0 - i) /(nCards - 1)
        iconImage = Image.open(icons[j])
        iconResized = iconImage.resize((iconWidth, iconHeight))
        j0 += 1

        x1 = int(x0 + r1*cos(angle))
        y1 = int(y0 - r1*sin(angle))
        image.paste(iconResized, (x1  - iconWidth // 2, y1 - iconHeight // 2), mask=iconResized)

        x1 = int(x0 + r0*cos(angle))
        y1 = int(y0 - r0*sin(angle))
        move = moves[i][j]
        if move > 5: move -= 11
        moveMag = abs(move)
        text = "{}".format(moveMag)
        textWidth, textHeight = font.getsize(text)
        draw.text((x1 - textWidth//2, y1 - textHeight//2 - 4), text, fill = (0,0,0), font=font)

        draw.arc([(x1-40, y1-40),(x1+40,y1+40)], -60, 60, fill = (0,0,0), width = 3)
        draw.arc([(x1-40, y1-40),(x1+40,y1+40)], 120, 240, fill = (0,0,0), width = 3)

        # draw arrow heads
        s = 1
        if move < 0: s = -1
        # +1 for clockwise
        # -1 for anti-clockwise
        
        x2 = x1 + 16
        y2 = y1 + 38 * s
        xy = [(x2, y2), (x2+16, y2-8*s), (x2+8, y2-16*s)]
        draw.polygon(xy, fill = (0,0,0), outline = (0,0,0))

        x2 = x1 - 16
        y2 = y1 - 38 * s
        xy = [(x2, y2), (x2-16, y2+8*s), (x2-8, y2+16*s)]
        draw.polygon(xy, fill = (0,0,0), outline = (0,0,0))

    image.save("back{:02d}.png".format(i))

    #front of card
    image = Image.new("RGB", imageSize, (255, 255, 255))
    iconImage = Image.open(icons[i])
    iconResized = iconImage.resize((frontWidth, frontWidth), resample=Image.BICUBIC)
    image.paste(iconResized, (x0 - frontWidth // 2, y0 - frontWidth // 2), mask = iconResized)

    draw = ImageDraw.Draw(image)
    
    #border
    draw.rectangle([(1,1),(imageSize[0]-2, imageSize[1]-2)], outline=(0,0,0), width = 1)
    draw.rectangle([(0,0),(imageSize[0]-1, imageSize[1]-1)], outline=(120,120,120), width = 1)
    
    image.save("front{:02d}.png".format(i))

# panelise into 3 large images for printing
for panelIndex in [0, 1, 2]:
    panelWidth = imageSize[1] * 2
    panelHeight = imageSize[0] * 4
    panelImage = Image.new("RGB", (panelWidth, panelHeight))
    for i in range(4):
        j = panelIndex * 4 + i
        if j < 11:
            frontImage = Image.open("front{:02d}.png".format(j))
            backImage = Image.open("back{:02d}.png".format(j))
        else:
            frontImage = Image.open("cycle.png")
            backImage = Image.new("RGB",imageSize, (255,255,255))

        panelImage.paste(frontImage.rotate(90, expand=1), ((i % 2) * imageSize[1], (i // 2) * imageSize[0] * 2))
        panelImage.paste(backImage.rotate(90, expand=1), ((i % 2) * imageSize[1], ((i // 2) * 2 + 1) * imageSize[0]))

    panelImage.save("panel{}.png".format(panelIndex))
