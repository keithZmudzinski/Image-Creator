from gradient import *
from shapes import *
from PIL import Image, ImageDraw


dims = (200,1000)
colors = [(230,230,255),(0,0,255)]
colors = gradientListColrs(colors, dims[0])
print(colors)

img = gradientDraw(colors,'TlBr', dims)
img.save("mainTest.png")

img2,list = makeTDrop(img,4,(0,600),dims[0]/2,'red')

test = outlineTDrop(img2,list)
test.save('hope.png')
