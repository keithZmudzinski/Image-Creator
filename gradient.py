from PIL import Image, ImageDraw
#POSSIBLE STRINGS FOR 'shape':
#   'LR': Left to right, 'TB': Top to Bottom,
#   'TlBr': Top left to Bottom Right, 'BlTr': Bottom left to Top right
#   NOTE: ONLY WORKS FOR IMGS WITH WIDTH >= HEIGHT :(
def gradientDraw(colors, img, shape, dims):
    """Takes list of colors, draws on img, a shape with dims dimensions"""
    draw = ImageDraw.Draw(img)
    dimX,dimY = dims
    j = 1
    if(shape == "LR"):
        for xCo in range(dimX):
            if(xCo >= (dimX/len(colors))*j):
                j += 1
            draw.line([(xCo,0),(xCo,dimY)],fill =(colors[j-1]),width = 1)
    elif(shape == "TB"):
        for yCo in range(dimY):
            if(yCo >= (dimY/len(colors))*j):
                j += 1
            draw.line([(0,yCo),(dimX, yCo)],fill =(colors[j-1]),width = 1)
    elif(shape == "TlBr"):
        flip = 2
        slope = dimY/dimX
        dist = max(dimX,dimY)
        if(dist == dimY):
            flip = .5
        for i in range(dimX+1):
            if(i >= (dist/len(colors))*flip*j):#only go 1/2 way
                j += 1
            draw.line([(i,0), (0,slope*i)],fill =(colors[j-1]),width = 1)
            draw.line([(dimX - i,dimY), (dimX,(slope*(dimX-i)))],fill =(colors[len(colors)-(j-1)-1]),width = 1)
    elif(shape == "BlTr"):
        for smaller in range(min(dimX,dimY)):
            if(smaller >= (min(dimX,dimY)/len(colors))*j*2):#only go 1/2 way
                j += 1
            draw.line([(0,smaller),(dimX-smaller,dimY)], fill = colors[round(len(colors)/2) - j], width = 1)
            draw.line([(dimX,dimY-smaller),(smaller,0)], fill = colors[round(len(colors)/2) + j-2], width = 1)

def gradientListColrs(colors,steps):
    """Returns list of RGB tuples transitioning through all colors in colors\n
        in N steps"""
    if(not(colors) or steps < len(colors)-1): #empty list or too few steps for amount of colors
        return -1
    if(len(colors) == 1): #list of size 1 returns list of that color
        L = [color for int in range(steps)]
        return L
    colorList = [] #list of at least size 2
    for i,color in enumerate(colors):
        if(i != len(colors)-1):
            colorList += (gradient2Colrs(colors[i], colors[i+1],steps/(len(colors)-1)))
    return colorList

#Steps is number of transitions between the colors
#   Actual number will be +-1 due to rounding
def gradient2Colrs(c1, c2, steps):
    """Returns list of RGB tuples transitioning from c1 to c2 in N steps"""
    steps = round(steps)
    colors = []
    diff = tuple(map(lambda t1,t2: (t2-t1)/steps, c1,c2))#get diff. bet. ea.
                                                    #tuple ele., div. by num. steps
    for i in range(steps+1):
        colors.append(tuple(map(lambda x,y: round(x + (y*i)),c1,diff)))
    return colors
