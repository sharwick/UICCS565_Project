import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from classes import Rect

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




def printFloorplan(rectangles,outfile):
	MINX = findMinX(rectangles)
	MAXX = findMaxX(rectangles)
	MINY = findMinY(rectangles)
	MAXY = findMaxY(rectangles)


	fig1 = plt.figure()
	ax1 = fig1.add_subplot(111, aspect='equal')
	ax1.set_xlim([MINX,MAXX])
	ax1.set_ylim([MINY,MAXY])
	#ax1.set_yticks([])
	#ax1.set_xticks([])

	for j in range(len(rectangles)):
		p = rectangles[j].makePatch()
		p.set_facecolor("#FF0000")

		if (rectangles[j].flag):
			p.set_facecolor("00FF00")
		#p.set_facecolor((rectangles[j].connectionsRatio,0,0))
		#p.set_facecolor((1,0,0))
		ax1.add_patch(p)


		
	fig1.savefig(outfile, dpi=90, bbox_inches='tight')


def test():
	R1 = Rect(1,0.1,0.5,0.5)
	R2 = Rect(0.6,0.7,0.2,0.1)
	R3 = Rect(0.5,0.7,0.1,0.1)
	R4 = Rect(0,0.7,0.1,0.1)

	myRectangles = [R1,R2,R3,R4]

	printFloorplan(myRectangles,'rect1.png')

#test()