from gradient import *
from shapes import *
from PIL import Image, ImageDraw


dims = (800,600)
colors = [(255,0,0),(50,0,0),(0,0,0)]
colors = gradientListColrs(colors, dims[0])

img = gradientDraw(colors,'BlTr', dims)
img.save("mainTest.png")

img2,list = makeTDrop(img,4,(0,600),dims[0]/2,'red')
print(list)
test = outlineTDrop(img2,list)
test.save('hope.png')
