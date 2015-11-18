import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

########################################################################
class Rect:
	def __init__(self,inX,inY,inW,inH):
		self.x = inX
		self.y = inY
		self.w = inW
		self.h = inH

	def makePatch(self):
		p = patches.Rectangle(
				(self.x,self.y),
				self.w,
				self.h,
				hatch='/',
	        	fill=True,	   
	        	facecolor="#959595", 
			)
		return p
########################################################################
def findMaxX(array):
	max=0

	for r in array:
		if (r.x+r.h>max):
			max = r.x+r.h

	return max

def findMaxY(array):
	max=0

	for r in array:
		if (r.y+r.h>max):
			max = r.y+r.h

	return max

def findMinX(array):
	min=100000000

	for r in array:
		if (r.x<min):
			min = r.x
		
	return min

def findMinY(array):
	min=100000000

	for r in array:
		if (r.y<min):
			min = r.y

	return min	
########################################################################

R1 = Rect(1,0.1,0.5,0.5)
R2 = Rect(0.6,0.7,0.2,0.1)
R3 = Rect(0.5,0.7,0.1,0.1)
R4 = Rect(0,0.7,0.1,0.1)

rectangles = [R1,R2,R3,R4]


MINX = findMinX(rectangles)
MAXX = findMaxX(rectangles)
MINY = findMinY(rectangles)
MAXY = findMaxY(rectangles)

print(MINX)
print(MAXX)
print(MINY)
print(MAXY)


def printFloorplan():

	fig1 = plt.figure()
	ax1 = fig1.add_subplot(111, aspect='equal')
	ax1.set_xlim([MINX,MAXX])
	ax1.set_ylim([MINY,MAXY])
	#ax1.set_yticks([])
	#ax1.set_xticks([])

	for j in range(len(rectangles)):
		ax1.add_patch(rectangles[j].makePatch())

	fig1.savefig('rect1.png', dpi=90, bbox_inches='tight')

printFloorplan()