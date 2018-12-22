from gradient import *
from shapes import *
from voronoi import *
from PIL import Image, ImageDraw


dims = (800,600)
colors = [(255, 191, 0,255),(123,221,0,255),(191, 0, 255,255)]
colors = gradientListColrs(colors, dims[1])
#
img = gradientDraw(colors,'TlBr', dims)
img1 = gradientDraw(colors,'LR',dims)
img2 = gradientDraw(colors,'BlTr',dims)
img3 = gradientDraw(colors,'TB',dims)
# tdrop,tdropList = makeTDrop(img,3,(0,50),100,'red')
# Timg = outlineTDrop(tdrop,tdropList)
# Timg.save('tdrop.png')
# img.save('banner.png')
points = [(433,233),(222,0),(100,500),(321,50)]
vlinesImg,regions = incDrawLines(points,dims)
vlinesImg.save('test.png')
[print(i,region) for i,region in enumerate(regions)]
collage = createCollage([img,img1,img2,img3],regions,points)
collage.save('collage.png')
#firstRegionImg = outlineRegion(img,regions[3],points[3])
#firstRegionImg.save('singleRegion.png')
