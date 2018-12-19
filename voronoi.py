'''Functions for creating voronoi regions'''
from PIL import Image, ImageDraw
import sys

def tuple1st(tup):
    return tup[0]

def lineFrmPnts(p1,p2):
    """Returns slope and y-intercept"""
    slope = (p2[1]-p1[1])/(p2[0]-p1[0])
    intercept = p2[1]-(slope*p2[0])
    return slope,intercept

def pntSlpe(pnt,slope):
    """Returns y-intercept of line"""
    return (pnt[1]-slope*pnt[0])

def invSlpe(slp):
    try:
        return -1/slp
    except ZeroDivisionError:
        sys.exit('Do not enter equidistant points. This results in an infinite slope')

def midpoint(p1,p2):
    return (round((p1[0]+p2[0])/2),round((p1[1]+p2[1])/2))

def distance(p1,p2):
    return ((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)**.5


def getX(ele):
    return ele[0][0]

def sortAdjs(adjList):
    srted = sorted(adjList,key = getX)
    return srted

def Y2X(y,b,m):
    return (y-b)/m

def checkAllDistances(p1,p2,line,points):
    correctDist = (distance(p1,line) + distance(p2,line))/2
    for i,point in enumerate(points):
        if( correctDist > distance(line,point)#if closer to another point
        and point != p1#and that point not orig pnt or clsst you're checking
        and point != p2):   #against
            return False            #because they ran into vertex[0]'s area
    return True

def insideImg(point,dims):
    #if 0 <= x <= maxX and 0 <= y <= maxY
    return (point[0] <= dims[0] and point[0] >= 0
        and point[1] <= dims[1] and point[1] >= 0)

def changeCoord(pnt,dims,orig,clsst,slope,intercept,dir,points):
    '''Returns two points, first and last valid points of line in direction dir'''
    x,y = pnt
    validx1 = 0
    validx2 = 0
    validy1 = 0
    validy2 = 0
    i = 0
    while(insideImg((x,y),dims)#start checking if pnt in frame, not valid
    and not(checkAllDistances(orig,clsst,(x,y),points))):
        x += 1*dir
        y= slope*x + intercept
    while (insideImg((x,y),dims)#if in frame and valid
    and checkAllDistances(orig,clsst,(x,y),points)):
        if i == 0:#first valid point
            validx1,validy1 = x,y
            i += 1
        x += 1*dir
        y= slope*x + intercept
    validx2,validy2 = x - 1*dir,slope*x + intercept#last valid point
    return ((validx1,validy1),(validx2,validy2))

def incDrawLines(points,dims):
    '''Given list of point tuples and dims of image,
    return image with voronoi lines drawn on it'''
    img = Image.new('RGBA', dims, color = 'white')
    draw = ImageDraw.Draw(img)
    for point in points:
        for otherPoint in points:
            if point == otherPoint:
                break
            midpnt = midpoint(point,otherPoint)
            x,y = midpnt
            #slope and intercept for line bet midoint and orig vertex
            slope,intercept = lineFrmPnts(point,midpnt)
            slope = round(invSlpe(slope),1)#get normal to slope
            intercept = pntSlpe(midpnt,slope)#get y-int for normal to slope
            pnt1Pos,pnt2Pos = changeCoord((x,y),dims,point,otherPoint,slope,intercept,1,points)
            pnt1Neg,pnt2Neg = changeCoord((x,y),dims,point,otherPoint,slope,intercept,-1,points)
            if(pnt1Pos != pnt2Pos and pnt1Neg != pnt2Neg):
                if(pnt1Pos != (0,0) and pnt2Pos != (0,0)):
                    draw.line([pnt1Pos,pnt2Pos],fill = 'black', width = 1)
                if(pnt1Neg != (0,0) and pnt2Neg != (0,0)):
                    draw.line([pnt1Neg,pnt2Neg],fill = 'black', width = 1)
    return img
