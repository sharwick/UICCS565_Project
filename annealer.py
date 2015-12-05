########################################################################
#	Annealing algorithm based on class notes (L08_fp-fp2.pdf)
########################################################################

import utils
import time
import math
import random
import metrics
import classes
from copy import copy, deepcopy
from initializeMatchPairs import initializeMatchPairs
import printFloorplan as pfp

annealingParameters = classes.AnnealingParameters(100,.85,5,.05,1,1)



#####################################################################################################################
# METHOD 1: Flip a random chain (random length) of operators
def updateSolutionRandomChain(root,rectangles,dictionary):
	polishArray = utils.getPolishArray(root)

	# Choose random number from 0 to n-2
	m = random.randint(0,len(rectangles)-2)
	n = random.randint(m,len(rectangles)-2)
	count = -1
	index = 0

	while (count<n):
		index += 1 # must increment from previous round

		while polishArray[index] != '-' and polishArray[index] != '|':
			index += 1

		count += 1

		if (count>m):
			if polishArray[index] == '-':
				polishArray[index] = '|'
			else:
				polishArray[index] = '-'

	newRoot = utils.getTreeFromPolishArray(polishArray,rectangles,dictionary)

	return newRoot;

#####################################################################################################################
# Find a node where the right node can fit within the white space of the left and collapse that subtree 1 node
def updateSolutionFitNode(root,rectangles,dictionary):
	newRoot = deepcopy(root)


	# Fit in and remove a (parent) node if possible
#	if root.left is not None:
#		if fitRightInLeft(newRoot.left):
#			fitRect = newRoot.left.right
#			newRoot.left = newRoot.left.left
#			newRoot.left.fitRect = fitRect

	
	# Other thoughts:
	# Check right tree for a node that fits in top right portion of left module
	# Create new node containing old modules on bottom/left and new nodes on top/right


	

	def _helperUpdateSolutionFitNode(root):
		# Try left and then right
		if root.left is not None:
			if fitRightInLeft(newRoot.left):
				fitRect = newRoot.left.right
				newRoot.left = newRoot.left.left
				newRoot.left.fitRect = fitRect
				return True
			if _helperUpdateSolutionFitNode(root.left):
				return True

		elif root.right is not None:
			if fitRightInLeft(newRoot.right):
				fitRect = newRoot.right.right
				newRoot.right = newRoot.right.left
				newRoot.right.fitRect = fitRect
				return True
			if _helperUpdateSolutionFitNode(root.right):
				return True


		return False

	if _helperUpdateSolutionFitNode(newRoot):
		print("Fit Node succeeded")

	return newRoot

def fitRightInLeft(node):
	if node.left is None or node.right is None:
		return False

	if node.left.type == 'rect':
		return False

	if node.left.whiteArea > node.right.getArea() and node.left.whiteLength>=max(node.right.w,node.right.h):
		return True

	return False
#####################################################################################################################





def anneal(dataset, annealingParameters, cost, outputPrefix,scenario):
	# Solutions will be represented by roots to a slicing tree

	# Setup
	updateMethods = [updateSolutionRandomChain,updateSolutionFitNode]
	#updateMethods = [updateSolutionRandomChain]
	start = time.time()
	(initialSolution, rectangles, dictionary, matrix) = initializeMatchPairs(dataset)
	count = 0

	currentSolution = initialSolution
	bestSolution = initialSolution
	T = annealingParameters.T
	M = 0
	MT = 1
	uphill = 0
	n = len(rectangles)
	N = annealingParameters.k * n
	reject=0
	timeDiff = time.time() - start

	#Iterations
	while (reject/MT <= 1-annealingParameters.thresholdAccepted) and T>=annealingParameters.thresholdTemp and timeDiff<=annealingParameters.thresholdTime:

		MT = 1 # start at 1 to avoid divide by 0
		uphill = 0
		reject = 0

		timeDiff = time.time() - start

		
		while uphill<=N and MT<=2*N:
			#newSolution = updateSolutionRandomChain(currentSolution,rectangles,dictionary)
			#newSolution = updateSolutionFitNode(currentSolution,rectangles,dictionary)

			# randomly choose which method to use for updating
			randomIndex = random.randint(0,len(updateMethods)-1)
			newSolution = updateMethods[randomIndex](currentSolution,rectangles,dictionary)

			#print(cost(newSolution))
			count+=1 # to track total iterations.  Should not be updated elsewhere.

			MT += 1
			deltaCost = cost(newSolution) - cost(currentSolution)

			# Updates
			if deltaCost <= 0 or random.uniform(0,1) < math.exp(-deltaCost/T):
				if deltaCost>0:
					uphill += 1

				currentSolution = newSolution

				if cost(currentSolution)<cost(bestSolution):
					bestSolution = currentSolution
			else:
				reject += 1
	
			timeDiff = time.time() - start

			if bestSolution == currentSolution:
				print(dataset + ':  ' + str(count) + '= ' + str(cost(bestSolution)) + '  T=' + str(T) + '  timeDiff=' + str(timeDiff))

		T = annealingParameters.r*T

	newRectangles = []
	def constructNewRectangleMatrix(node):
		if node.type == 'rect':
			newRectangles.append(node.rect)
		else:
			if node.fitRect is not None:
					constructNewRectangleMatrix(node.left.fitRect)
			if node.left is not None:
				constructNewRectangleMatrix(node.left)
			if node.right is not None:
				constructNewRectangleMatrix(node.right)


	constructNewRectangleMatrix(bestSolution)

	print("Total area for " + dataset + " = " + str(bestSolution.w*bestSolution.h))
	pfp.printFloorplan(newRectangles,dataset,outputPrefix + dataset + '.png',scenario)

	return (bestSolution, rectangles, dictionary, matrix)




# Run this analysis for all benchmarks
def analyzeAllBenchmarks():
	for dataset in utils.benchmarks:
		print("Starting benchmark analysis: " + dataset)
		anneal(dataset, annealingParameters,metrics.costArea)
#analyzeAllBenchmarks()
#anneal(utils.benchmarks[0], annealingParameters,metrics.costArea)
#anneal('ami49', annealingParameters,metrics.costArea)
#anneal(utils.benchmarks[4], annealingParameters,metrics.costArea)