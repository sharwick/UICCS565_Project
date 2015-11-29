import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from classes import Rect
import metrics

def findMaxX(array):
	maxValue=0

	for r in array:
		if (r.x+r.w>maxValue):
			maxValue = r.x+r.w

	return maxValue

def findMaxY(array):
	maxValue=0

	for r in array:
		if (r.y+r.h>maxValue):
			maxValue = r.y+r.h

	return maxValue

def findMinX(array):
	minValue=100000000

	for r in array:
		if (r.x<minValue):
			minValue = r.x
		
	return minValue

def findMinY(array):
	minValue=100000000

	for r in array:
		if (r.y<minValue):
			minValue = r.y

	return minValue	
########################################################################




def printFloorplan(rectangles,dataset, outfile,scenario):
	MINX = findMinX(rectangles)
	MAXX = findMaxX(rectangles)
	MINY = findMinY(rectangles)
	MAXY = findMaxY(rectangles)

	#print(dataset + '|' + str(MINX) + '|' + str(MAXX) + '|' + str(MINY) + '|' + str(MAXY))


	fig1 = plt.figure()
	fig1.suptitle("Floorplan for "+dataset+' Benchmark\n'+scenario, fontsize=14, fontweight='bold')		

	ax1 = fig1.add_subplot(111, aspect='equal')
	ax1.set_xlim([MINX,MAXX])
	ax1.set_ylim([MINY,MAXY])
	ax1.set_yticks([])
	ax1.set_xticks([])

	for j in range(len(rectangles)):
		p = rectangles[j].makePatch()
		p.set_facecolor("#FF0000")

		if (rectangles[j].flag):
			p.set_facecolor("00FF00")
		#p.set_facecolor((rectangles[j].connectionsRatio,0,0))
		#p.set_facecolor((1,0,0))
		ax1.add_patch(p)


	coverage = metrics.getCoverage(rectangles)
	coveragepct = (coverage*1.0)/(MAXX*MAXY)*100
	#print(str(coverage))
	#print(str(coveragepct))
	#print(str(MAXX*MAXY))
	ax1.set_xlabel('Area = ' + str(MAXX*MAXY) + ' = ' + str(MAXX) + ' x ' + str(MAXY) + '\nCoverage = ' + str("{0:.0f}%".format(coveragepct)))

	fig1.savefig(outfile, dpi=90, bbox_inches='tight')


def test():
	R1 = Rect(1,0.1,0.5,0.5)
	R2 = Rect(0.6,0.7,0.2,0.1)
	R3 = Rect(0.5,0.7,0.1,0.1)
	R4 = Rect(0,0.7,0.1,0.1)

	myRectangles = [R1,R2,R3,R4]

	printFloorplan(myRectangles,'rect1','rect1.png','Test')

#test()