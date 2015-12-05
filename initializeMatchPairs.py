############################################################################
# This algorithm will read data and create an initial floorplan
# by grouping pairs of modules based on their connectivity.


import parseData as pd
import printFloorplan as pfp
import numpy as np
import utils
from copy import copy, deepcopy
from classes import Rect, RectNode



def initializeMatchPairs(dataset):

	# Import data for benchmark
	(rectangles,netlists,dictionary,matrix)	= pd.createAllBaseData(dataset)

	# Stack pairs of modules vertically or horizontally.  Iterate through all modules in order of descending connectivity.
	matrixWorkingCopy = deepcopy(matrix)
	nodes = []

	while np.max(matrixWorkingCopy) > -1:
		(i,j) = utils.getMaxOfMatrix(matrixWorkingCopy)

		if i==j:
			# end case, since this value has to be 0
			node = RectNode(None,None,'rect',rectangles[i])
			nodes.append(node)
			#matrixWorkingCopy[i,i] = -1

			# Nullify considered modules
			for k in range(len(rectangles)):
				matrixWorkingCopy[i,k] = -1
				matrixWorkingCopy[k,i] = -1

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

			#Default I and J to same origin [will I need this?]
			rectI.x = newX
			rectI.y = newY
			rectJ.x = newX
			rectJ.y = newY
			
			type = utils.optimizeTwoRectangles(rectI,rectJ)			

			nodeI = RectNode(None,None,'rect',rectI)
			nodeJ = RectNode(None,None,'rect',rectJ)
			node = RectNode(nodeI,nodeJ,type,None)
			nodes.append(node)

	def printRectangleTest():
		for r in rectangles:
			print(r.name + '|' + str(r.x) + '|' + str(r.y) + '|' + str(r.w) + '|' + str(r.h))
	#printRectangleTest()

	# Given initial grouping of modules, construct a full slicing tree
	while (len(nodes)>1):
		length = len(nodes)
		newNodes = []

		# sort the nodes
		nodes = sorted(nodes,key=utils.sortByShape)

		# Create new layer in tree
		for i in xrange(0,len(nodes)-1,2):
			left = nodes[i]
			right = nodes[i+1]

			def newModuleMethod():
				stack = utils.optimizeTwoRectangles(left,right)
				return stack

			def oldModuleMethod():
				# Choose split direction that will minimize area (unless it violates skewness)
				verticalStackArea = max(left.w,right.w)*(left.h+right.h)
				horizontalStackArea = max(left.h,right.h)*(left.w+right.w) 
				stack = '|'

				if horizontalStackArea<verticalStackArea:
					stack='-'
				return stack

			#stack = oldModuleMethod()
			stack = newModuleMethod()

			def ensureSkew():
				# Ensure that we are creating a skew tree
				if right.type != 'rect':
					if right.type == '-':
						stack = '|'
					else:
						stack = '-'
			ensureSkew()

			newNode = RectNode(left,right,stack,None)
			newNodes.append(newNode)
		# Handle edge case where there is an unmatched odd node
		if len(newNodes)*2<len(nodes):
			# Create new node with left = previous node and right = remaining node. This will prevent dangling node.
			prevNode = newNodes[len(newNodes)-1]
			remainingNode = nodes[len(nodes)-1]

			if remainingNode.type == 'rect':
				remainingNode.rect.flag = True
			
			#print(dataset + '  ' + remainingNode.type + '  ' + str(len(rectangles)))


			newNode = RectNode(prevNode,remainingNode,prevNode.type,None)
			newNodes.pop() # avoid duplicate rectangles
			newNodes.append(newNode)
			#newNodes.append(nodes[len(nodes)-1])

		nodes = newNodes

	root = nodes[0] # tree has been created

	utils.resetRectangles(rectangles)
	utils.updateTreeDimensions(root)

	def printTest():
		print(utils.getPolish(root))
		print(root.w)
		print(root.h)
		print(root.getArea())
	#printTest()
	

	def checkPolishArray():
		print(utils.getPolishArray(root))
		polishArray = utils.getPolishArray(root)
		newTree = utils.getTreeFromPolishArray(polishArray,rectangles,dictionary)
		print("**************************************")
		print(utils.getPolishArray(newTree))
	#checkPolishArray()

	pfp.printFloorplan(rectangles,dataset,"Output/initialMatchPairs_" + dataset + ".png",'Initial Floorplan')

	return (root, rectangles, dictionary, matrix)


# Run this analysis for all benchmarks
def analyzeAllBenchmarks():
	for dataset in utils.benchmarks:
		initializeMatchPairs(dataset)
#analyzeAllBenchmarks()

#initializeMatchPairs(utils.benchmarks[0])