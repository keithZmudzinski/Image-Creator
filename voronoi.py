'''Functions for creating voronoi regions'''
from PIL import Image, ImageDraw
import sys

def tuple1st(tup):
    return tup[0]

def lineFrmPnts(p1,p2):
    """Returns slope and y-intercept"""
    slpe = slope(p1,p2)
    intercept = p2[1]-(slpe*p2[0])
    return slpe,intercept

def slope(p1,p2):
    return (p2[1]-p1[1])/(p2[0]-p1[0])
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
    validx2,validy2 = x - 1*dir,slope*(x - 1*dir) + intercept#last valid point
    #validx2,validy2 = x,y#last invalid point
    return ((validx1,validy1),(validx2,validy2))

def incDrawLines(points,dims):
    '''Given list of point tuples and dims of image,
    return image with voronoi lines drawn on it'''
    img = Image.new('RGBA', dims, color = 'white')
    draw = ImageDraw.Draw(img)
    regions = [list() for point in points]
    for i, point in enumerate(points):
        for otherPoint in points:
            if point == otherPoint:
                continue
            midpnt = midpoint(point,otherPoint)
            x,y = midpnt
            #slope and intercept for line bet midoint and orig vertex
            slope,intercept = lineFrmPnts(point,midpnt)
            slope = round(slope,1)
            slope = round(invSlpe(slope),1)#get normal to slope
            intercept = pntSlpe(midpnt,slope)#get y-int for normal to slope
            pnt1Pos,pnt2Pos = changeCoord((x,y),dims,point,otherPoint,slope,intercept,1,points)
            pnt1Neg,pnt2Neg = changeCoord((x,y),dims,point,otherPoint,slope,intercept,-1,points)
            if(pnt1Pos != pnt2Pos and pnt1Neg != pnt2Neg):
                if(pnt1Pos != (0,0) and pnt2Pos != (0,0)):
                    draw.line([pnt1Pos,pnt2Pos],fill = 'black', width = 1)
                    regions[i].append((pnt1Pos,pnt2Pos))
                if(pnt1Neg != (0,0) and pnt2Neg != (0,0)):
                    draw.line([pnt1Neg,pnt2Neg],fill = 'black', width = 1)
                    regions[i].append((pnt1Neg,pnt2Neg))
    return img,regions


def createCollage(imgList,regionList,points):
    '''Returns new image'''
    #imgList: list of PIL image objects
        #imgList size should be equal to regionList size
        #each img in imgList needs to be of same size
    #regionList: list of region lists
        #will have same size as points
        #each region in regionList defines 1 region
        #obtain regionList from 2nd returned value of incDrawLines
    #points: list of user specified points; [(x1,y1),(x2,y2),...]
        #All points should fall within specified dimensions
    #NOTE: when creating images and regions, use the same dimensions for both
        #this ensures the regions allign and fill up the given images
    if len(imgList) != len(regionList) or len(regionList) != len(points):
        raise ValueError('imgList or regionList or points not of same size',
            len(imgList),len(regionList),len(points))
    finalImg = imgList[0]
    for i,img in enumerate(imgList):
        imgTemp = outlineRegion(img,regionList[i],points[i])
        finalImg = Image.alpha_composite(finalImg,imgTemp)
    return finalImg

def outlineRegion(img,region,point):
    '''Outlines given region on given img, returns new image'''
    #img: PIL img class,should be the img you want region
        #to be cut out of
        #all imgs used for given final img should be of same size
        #does not alter image, returns new image
    #region: list of tuples, tuples consist of start and end point
        #[((x1,y1),(x2,y2)),...]
    #point: coresponding voronoi point to the defined region
    imgCopy = img.copy()
    draw = ImageDraw.Draw(imgCopy)
    dims = imgCopy.size
    for line in region:
        slope,intercept = lineFrmPnts(line[0],line[1])
        offset = min(line[0][0],line[1][0])
        interval = abs(line[0][0] - line[1][0])
        y = slope*point[0] + intercept
        if y > point[1]:#need to erase downwards
            if slope < 0:#need to erase to the right
                for i in range(0,interval):
                    x = i + offset
                    y = slope*x + intercept
                    #draw.line(((x,y),(x,dims[1])),fill = (0,0,0,0),width = 1)
                    draw.rectangle([(x,y),(dims[0],dims[1])],fill = (0,0,0,0))
            else:#erase to the Left
                for i in range(0,interval):
                    x = i + offset
                    y = slope*x + intercept
                    draw.rectangle([(x,y),(0,dims[1])],fill = (0,0,0,0))
        else:#erase upwards
            if slope < 0:#erase to the left
                for i in range(0,interval):
                    x = i + offset
                    y = slope*x + intercept
                    draw.rectangle([(x,y),(0,0)],fill = (0,0,0,0))
                    #draw.line(((x,y),(x,0)),fill = (0,0,0,0),width = 1)
            else:#erase to the right
                for i in range(0,interval):
                    x = i + offset
                    y = slope*x + intercept
                    draw.rectangle([(x,y),(dims[0],0)],fill = (0,0,0,0))
        #ERASE SIDEWAYS, FLIP THE AXES AND DO SAME THING AGAIN
    return imgCopy
