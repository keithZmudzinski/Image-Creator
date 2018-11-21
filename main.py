from gradient import *
from shapes import *
from PIL import Image, ImageDraw


dims = (8000,500)
colors = [(0,123,255,255),(0,123,255,150),(255, 255, 255,0)]
colors = gradientListColrs(colors, dims[1])
img = gradientDraw(colors,'TB', dims)
img.save('banner.png')
