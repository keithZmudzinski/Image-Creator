from gradient import *
from shapes import *
from voronoi import *
from PIL import Image, ImageDraw


dims = (1920,1080)
points = [(305,249),(191,803),(1107,400),(1000,900)]
colors = [(255, 102, 179,255),(255, 153, 51,255)]#(191, 0, 255,255)]
colors = gradientListColrs(colors, dims[1])
#
img = gradientDraw(colors,'BlTr', dims)
img1 = gradientDraw(colors,'TlBr',dims)
colors = [(255, 153, 51,255),(255, 102, 179,255)]
colors = gradientListColrs(colors,dims[1])
img2 = gradientDraw(colors,'LR',dims)
img3 = gradientDraw(colors,'LR',dims)
# tdrop,tdropList = makeTDrop(img,3,(0,50),100,'red')
# Timg = outlineTDrop(tdrop,tdropList)
# Timg.save('tdrop.png')
# img.save('banner.png')

vlinesImg,regions = incDrawLines(points,dims)
vlinesImg.save('test.png')
[print(i,region) for i,region in enumerate(regions)]
collage = createCollage([img,img1,img2,img3],regions,points)
collage.save('collage.png')
#firstRegionImg = outlineRegion(img,regions[3],points[3])
#firstRegionImg.save('singleRegion.png')
