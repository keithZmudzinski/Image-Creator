"""Functions for creating 2d shapes"""
from PIL import Image, ImageDraw
import math


def frange(width, step):
    """Allows fractional steps in range"""
    start,stop = width
    while start < stop:
        yield start
        start += step

def makeTDrop(m,domain,multiplier):
    """Returns t-drop image"""
    #final img dim = (multiplier*2,multiplier*2)
        #higher num makes finer line
    #larger domain repeats points more,
        #better for finer lines
    points = []
    maxY = 0
    step = .0009 #Used to create closer together points (more points = better)

    for i in frange(domain,step):
        points.append(round(math.cos(i)*multiplier))
        points.append(round(math.sin(i)*math.sin(.5*i)**m*multiplier))
    minimum = min(points)
    if(minimum < 0):#makes all points non-negative to fit on canvas
        minimum *= -1
        points = list(map(lambda t: t + minimum,points))
    maximum = max(points)
    img = Image.new('RGBA',(maximum,maximum),color = (255,255,255,255))
    draw = ImageDraw.Draw(img)
    draw.point(points,fill = "black")
    return img
img = makeTDrop(4,(0,60), 150)
print("Size: ", img.size)
img.save("test.png")
