############################################################################
# This algorithm will read data and create an initial floorplan
# by grouping pairs of modules based on their connectivity.


import parseData as pd
import printFloorplan as pfp
import numpy as np
import utils
from copy import copy, deepcopy
from classes import Rect, RectNode



# Import data for benchmark
benchmark = 'ami33'
(rectangles,netlists,dictionary,matrix)	= pd.createAllBaseData(benchmark)



def try1():
	# Diagonalize
	pd.diagonalizeRectangles(rectangles)


	# Stack pairs of modules vertically or horizontally.  Iterate through all modules in order of descending connectivity.
	matrixWorkingCopy = deepcopy(matrix)
	newRectangles = []

	while np.max(matrixWorkingCopy) > -1:
		print(utils.getMaxOfMatrix(matrixWorkingCopy))
		(i,j) = utils.getMaxOfMatrix(matrixWorkingCopy)

		if i==j:
			newRectangles.append(rectangles[i])
			matrixWorkingCopy[i,i] = -1

		else:
			rectI = rectangles[i]
			rectJ = rectangles[j]

			# Nullify considered modules
			for k in range(len(rectangles)):
				matrixWorkingCopy[i,k] = -1
				matrixWorkingCopy[j,k] = -1
				matrixWorkingCopy[k,i] = -1
				matrixWorkingCopy[k,j] = -1

			# Create new intermediate modules that contain the merged modules
			newX = min(rectI.x,rectJ.x)
			newY = min(rectI.y,rectJ.y)

			verticalStackArea = max(rectI.w,rectJ.w)*(rectI.h+rectJ.h)
			horizontalStackArea = max(rectI.h,rectJ.h)*(rectI.w+rectJ.w)

			if (verticalStackArea>horizontalStackArea):
				newH = max(rectI.y,rectJ.y)
				newW = rectI.w + rectJ.w

				# Modify the existing rectangles (i.e., move j)
				rectJ.x = rectI.x+rectI.w
				rectJ.y = rectI.y
				
			else:
				newH = max(rectI.y,rectJ.y)
				newW = rectI.w + rectJ.w

				# Modify the existing rectangles (i.e., move j)
				rectJ.x = rectI.x
				rectJ.y = rectI.y+rectI.h
				
			newName = rectI.name + "," + rectJ.name
			newRect = Rect(newX,newY,newH,newW,newName)	
			newRectangles.append(newRect)

	# Remove space
	#for r in rectangles:

	pfp.printFloorplan(rectangles,"Output/temp.png")


def try2():
	# Stack pairs of modules vertically or horizontally.  Iterate through all modules in order of descending connectivity.
	matrixWorkingCopy = deepcopy(matrix)
	nodes = []

	while np.max(matrixWorkingCopy) > -1:
		#print(utils.getMaxOfMatrix(matrixWorkingCopy)) # TEST
		(i,j) = utils.getMaxOfMatrix(matrixWorkingCopy)

		if i==j:
			node = RectNode(None,None,'rect',rectangles[i])
			nodes.append(node)
			matrixWorkingCopy[i,i] = -1

		else:
			rectI = rectangles[i]
			rectJ = rectangles[j]

			# Nullify considered modules
			for k in range(len(rectangles)):
				matrixWorkingCopy[i,k] = -1
				matrixWorkingCopy[j,k] = -1
				matrixWorkingCopy[k,i] = -1
				matrixWorkingCopy[k,j] = -1

			# Create new intermediate modules that contain the merged modules
			newX = min(rectI.x,rectJ.x)
			newY = min(rectI.y,rectJ.y)

			verticalStackArea = max(rectI.w,rectJ.w)*(rectI.h+rectJ.h)
			horizontalStackArea = max(rectI.h,rectJ.h)*(rectI.w+rectJ.w)
			type = ''

			if (verticalStackArea>horizontalStackArea):
				newH = max(rectI.y,rectJ.y)
				newW = rectI.w + rectJ.w
				type = '-'

				# Modify the existing rectangles (i.e., move j)
				rectJ.x = rectI.x+rectI.w
				rectJ.y = rectI.y
				
			else:
				newH = max(rectI.y,rectJ.y)
				newW = rectI.w + rectJ.w
				type = '|'

				# Modify the existing rectangles (i.e., move j)
				rectJ.x = rectI.x
				rectJ.y = rectI.y+rectI.h
				

			nodeI = RectNode(None,None,'rect',rectI)
			nodeJ = RectNode(None,None,'rect',rectJ)
			node = RectNode(nodeI,nodeJ,type,None)
			nodes.append(node)

	while (len(nodes)>1):
		length = len(nodes)
		newNodes = []

		# Create new layer in tree
		for i in xrange(0,len(nodes)-1,2):
			newNode = RectNode(nodes[i],nodes[i+1],'-',None)
			newNodes.append(newNode)
		# Handle edge case where there is an unmatched odd node
		if len(newNodes)*2<len(nodes):
			newNodes.append(nodes[len(nodes)-1])

		nodes = newNodes

	root = nodes[0]

	print(utils.getPolish(root))

try2()

