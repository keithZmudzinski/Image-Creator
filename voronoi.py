from scipy.spatial import Voronoi, voronoi_plot_2d
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import sys
points = [[128,455],[55,4],[455,56],[555,238],[400,555]]

def lineFrmPnts(p1,p2):
    """Returns slope and y-intercept"""
    slope = (p2[1]-p1[1])/(p2[0]-p1[0])
    intercept = p1[1]-(slope*p1[0])
    #print('slope', slope, 'intercept',intercept)
    return slope,intercept

def pntSlpe(pnt,slope):
    """Returns y-intercept of line"""
    return (pnt[1]-slope*pnt[0])

def invSlpe(slp):
    try:
        return -1/slp
    except ZeroDivisionError:
        sys.exit('Do not enter equidistant points. This results in an infinite slope')

def equiPoint(adjacent):
    p1,p2,p3 = adjacent
    m1 = midpoint(p1,p2)
    m2 = midpoint(p2,p3)
    m3 = midpoint(p1,p3)
    slope1,b1 = lineFrmPnts(p1,p2)
    slope2,b2 = lineFrmPnts(p2,p3)
    slope3,b3 = lineFrmPnts(p1,p3)
    slope1 = invSlpe(slope1)
    slope2 = invSlpe(slope2)
    slope3 = invSlpe(slope3)
    b1 = pntSlpe(m1,slope1)
    b2 = pntSlpe(m2,slope2)
    b3 = pntSlpe(m3,slope3)
    #print('slope1', slope1, 'slope2', slope2, 'slope3',slope3)
    y = ((b2*slope3-b1*slope3)/(slope1-slope2)) + b3
    x = (y-b1)/slope1
    return (x,y),slope1,slope3,b1,b3

def midpoint(p1,p2):
    return (round((p1[0]+p2[0])/2),round((p1[1]+p2[1])/2))

def distance(p1,p2):
    return ((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)**.5

def makeAdjList(points):
    orig = points
    orig1 = orig.copy()
    adj = []
    for point in orig:#for each point
        orig1.remove(point)
        min = distance(point, orig1[0])
        closest1 = orig1[0]
        closest2 = (sys.maxsize,sys.maxsize)
        for point1 in orig1:#get 2 closest points
            dist = distance(point1,point)
            if(dist < min):
                closest2 = closest1
                closest1 = point1
                min = dist
            elif(dist <= distance(point,closest2) and dist > min):
                closest2 = point1
        adj.append((point,closest1,closest2))
        orig1 = orig.copy()
    return adj#[(point,closest1,closest2),(p,c1,c2)...]

def getX(ele):
    return ele[0][0]

def sortAdjs(adjList):
    srted = sorted(adjList,key = getX)
    return srted

def Y2X(y,b,m):
    return (y-b)/m

def drawLines(adjList,dims):
    img = Image.new('RGBA', dims, color = 'white')
    for adj in adjList:
        if len(list) < 3:
            break
        pnt,c1,c2 = adj
        equi,slope1,slope2,b1,b2 = equiPoint(adj)
        m1 = midpoint(pnt,c1)
        m2 = midpoint(pnt,c2)
        #Really clean code for sure
        if((equi[0] < m1[0] and slope1 > 0) or (equi[0] > m1[0] and slope1 < 0)):
            y1 = dims[1]
        else:
            y1 = 0
        x1 = Y2X(y1,b1,slope1)
        if((equi[0] < m2[0] and slope2 > 0) or (equi[0] > m2[0] and slope2 < 0)):
            y2 = dims[1]
        else:
            y2 = 0
        x2 = Y2X(y2,b2,slope2)

        draw = ImageDraw.Draw(img)
        draw.line([(equi[0],equi[1]),(x1,y1)],fill = 'black',width = 1)
        draw.line([(equi[0],equi[1]),(x2,y2)],fill = 'black',width = 1)

    return img

list = sortAdjs(makeAdjList(points))
print(list)
img = drawLines(list,(800,600))
draw = ImageDraw.Draw(img)
for pointi in points:
    draw.point(pointi,fill = 'red')

img.save('xd.png')
