from PIL import Image, ImageDraw
#POSSIBLE STRINGS FOR 'shape':
#   'LR': Left to right, 'TB': Top to Bottom,
#   'TlBr': Top left to Bottom Right, 'BlTr': Bottom left to Top right
#   NOTE: ONLY WORKS FOR IMGS WITH WIDTH >= HEIGHT :(
def gradientDraw(colors, shape, dims):
    """Takes list of colors, draws on img, a shape with dims dimensions"""
    if(shape != 'LR' and shape != 'TB' and shape != 'TlBr' and shape != 'BlTr'):
        raise ValueError('Shape not one of four accepted values', shape)
    img = Image.new('RGBA',dims,color = 'white')
    draw = ImageDraw.Draw(img)
    dimX,dimY = dims
    j = 1
    if(shape == "LR"):# Vertical Gradient Left to Right
        for xCo in range(dimX):
            if(xCo >= (dimX/len(colors))*j):
                j += 1
            draw.line([(xCo,0),(xCo,dimY)],fill =(colors[j-1]),width = 1)
    elif(shape == "TB"):# Horizontal Gradient Top to Bottom
        for yCo in range(dimY):
            if(yCo >= (dimY/len(colors))*j):
                j += 1
            draw.line([(0,yCo),(dimX, yCo)],fill =(colors[j-1]),width = 1)
    elif(shape == "TlBr"):# Diagonal Gradient from TopLeft to BottomRight
        img = gradientBlTr(img,draw,dimX,dimY,colors)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
    elif(shape == "BlTr"):# Diagonal Gradient from BottomLeft to TopRight
        img = gradientBlTr(img,draw,dimX,dimY,colors)
    return img

def gradientBlTr(img,draw,dimX,dimY,colors):
    """Draws the gradient lines for the BlTr option,
        seperated because re-used for TlBr option"""
    slope = dimY/dimX
    lrger = max(dimX,dimY)
    if(lrger == dimY): #have to get slope recipricol for Portrait
        slope = 1/slope
    divider = lrger/len(colors) #used to step through colors
    j = 0
    for i in range(lrger):
        if(i > divider + (divider *j * 2)):#so use all colors no matter lrger size
            j += 1
        if(lrger == dimY):#if taller than wide (Portrait)
            draw.line([(i*slope,dimY),(0, dimY - i)],
                fill = colors[j],width = 1)
            draw.line([(i*slope,0),(dimX,dimY-i)],
                fill = colors[j + round(len(colors)/2) - 1],width = 1)
        else:#if wider than tall (Landscape)
            draw.line([(i,dimY),(0,round(dimY-(i*slope)))],
                fill = colors[j],width = 1)
            draw.line([(i,0),(dimX,round(dimY-(i*slope)))],
                fill = colors[j + round(len(colors)/2) - 1],width = 1)
    return img
def gradientListColrs(colors,steps):
    """Returns list of RGB tuples transitioning through all colors in colors\n
        in N steps"""
    #Good rule of thumb: set steps equal to one of the
    #   dimensions of the image you intend to use returned colorList on
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
