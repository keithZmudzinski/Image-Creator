from gradient import *
from shapes import *
from PIL import Image, ImageDraw


dims = (800,600)
colors = [(255, 191, 0,255),(191, 0, 255,255)]
colors = gradientListColrs(colors, dims[1])
img = gradientDraw(colors,'TB', dims)
img.save('banner.png')
