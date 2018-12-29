from gradient import *
from shapes import *
from voronoi import *
from PIL import Image, ImageDraw


dims = (1920,1080)
points = [(341,233),(479,681),(1555,181),(123,3),(1700,300),(1400,800)]

colors1 = [(0, 51, 153,255),(0,0,0,255)]
colors1 = gradientListColrs(colors1, dims[0])

colors2 = [(26,60,128,255),(0, 0, 0,255)]
colors2 = gradientListColrs(colors2,dims[0])

colors3 = [(0, 153, 102,255),(0, 0, 0,255)]
colors3 = gradientListColrs(colors3,dims[0])

colors4 = [(51,0,153,255),(0,0,0,255)]
colors4 = gradientListColrs(colors4,dims[0])

img1 = gradientDraw(colors1,'TlBr', dims)
img2 = gradientDraw(colors2,'TlBr',dims)
img3 = gradientDraw(colors3,'TlBr',dims)
img4 = gradientDraw(colors4,'TlBr',dims)
img5 = gradientDraw(colors3,'TlBr',dims)

vlinesImg,regions = incDrawLines(points,dims)
vlinesImg.save('test.png')
collage = createCollage([img1,img2,img1,img2,img3,img4],regions,points)
collage.save('collage.png')
