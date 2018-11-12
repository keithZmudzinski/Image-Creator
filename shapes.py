"""Functions for creating 2d shapes"""
from PIL import Image, ImageDraw
import math, sys


def frange(width, step):
    """Allows fractional steps in range"""
    start,stop = width
    while start < stop:
        yield start
        start += step

def makeTDrop(img,m,domain,multiplier,outline):
    """Returns t-drop image"""
    #draws tdrop on-top-of given image, does not alter original
    #m is how 'tear-droppy' it is; higher m = longer tail
    #larger domain repeats points more,
        #better for more solid lines
    #final img dim = (multiplier*2,multiplier*2)
        #higher num makes finer line
    step = .0009 #Used to create closer together points (more points = better)
    multiplier = round(multiplier)
    points = []
    img1 = img.copy()
    fillArray = [[0] * 3 for i in range(multiplier*2 + 1)]
    for x in range(len(fillArray)): #initialize array
        fillArray[x][0] = x #1st index holds x
        fillArray[x][1] = sys.maxsize #second holds maxY seen
        fillArray[x][2] = -sys.maxsize-1 #third holds minY seen
    for i in frange(domain,step):#calculates coord, makes fillArray to hld differences
        x = round(math.cos(i)*multiplier)
        y = round(math.sin(i)*math.sin(.5*i)**m*multiplier)
        points.append((x,y))
        if fillArray[x][1] > y:
            fillArray[x][1] = y
        if fillArray[x][2] < y:
            fillArray[x][2] = y
    minimum = min(points)
    minimum = min(minimum[0],minimum[1])
    if(minimum < 0):#makes all points non-negative to fit on canvas
        minimum *= -1
        points = list(map(lambda t: (t[0] + minimum,t[1] + minimum),points))
        minimum2 = min(points,key = lambda t:t[1])[1] #gets smallest y value
        points = list(map(lambda t: (t[0],t[1] - minimum2+1),points))#moves t-drop to top of frame
        fillArray = list(map(lambda t: (t[0],t[1] + minimum-minimum2+1, t[2] + minimum-minimum2),fillArray))
    maximum = max(points)
    maximum = max(maximum[0],maximum[1])
    draw = ImageDraw.Draw(img1)
    draw.point(points,fill = outline)
    return img1, fillArray

def outlineTDrop(img,list):
    img = img.copy()
    draw = ImageDraw.Draw(img)
    maxX = round(max(list,key = lambda t: t[0])[0]/2)#getlargestX 1/2
    width, height = img.size
    for i, coord in enumerate(list[0:round(len(list)/2)]):
        draw.line(((coord[0] + maxX,coord[1]+1),(coord[0] + maxX,0)),fill = (0,0,0,0),width = 1)
        draw.line(((coord[0] + maxX,coord[2]-1),(coord[0] + maxX,height)),fill = (0,0,0,0),width = 1)
    for i, coord in enumerate(list[round(len(list)/2):]):
        draw.line(((coord[0] - maxX,coord[1]+1),(coord[0] - maxX,0)),fill = (0,0,0,0),width = 1)
        draw.line(((coord[0] - maxX,coord[2]-1),(coord[0] - maxX,height)),fill = (0,0,0,0),width = 1)
    draw.rectangle([(maxX*2,0),(width,height)],fill = (0,0,0,0))
    return img
