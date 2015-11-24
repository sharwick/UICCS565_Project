########################################################################
#	Annealing algorithm based on class notes (L08_fp-fp2.pdf)
########################################################################

import utils
#import timeit
import time
import math
import random
import metrics
import classes
from copy import copy, deepcopy
from initializeMatchPairs import initializeMatchPairs
import printFloorplan as pfp

annealingParameters = classes.AnnealingParameters(100,.85,5,.05,2,1)


def updateSolution(root,rectangles,dictionary):
	polishArray = utils.getPolishArray(root)

	# Choose random number from 0 to n-2
	m = random.randint(0,len(rectangles)-2)
	count = -1
	index = 0

	while (count<m):
		index += 1 # must increment from previous round

		while polishArray[index] != '-' and polishArray[index] != '|':
			index += 1

		count += 1

	if polishArray[index] == '-':
		polishArray[index] = '|'
	else:
		polishArray[index] = '-'

	newRoot = utils.getTreeFromPolishArray(polishArray,rectangles,dictionary)

	return newRoot;


def anneal(dataset, annealingParameters, cost):
	# Solutions will be represented by roots to a slicing tree

	# Setup
	#start = timeit.default_timer()
	start = time.time()
	(initialSolution, rectangles, dictionary, matrix) = initializeMatchPairs(dataset)

	currentSolution = initialSolution
	bestSolution = initialSolution
	T = annealingParameters.T
	M = 0
	MT = 0
	uphill = 0
	n = len(rectangles)
	N = annealingParameters.k * n

	#Iterations
	while uphill<=N and MT<=2*N:

		MT = 1 # start at 1 to avoid divide by 0
		uphill = 0
		reject = 0

		#time = timeit.default_timer() - start
		timeDiff = time.time() - start

		while (reject/MT <= 1-annealingParameters.thresholdAccepted) and T>=annealingParameters.thresholdTemp and timeDiff<=annealingParameters.thresholdTime:

			newSolution = updateSolution(currentSolution,rectangles,dictionary)
			#print(cost(newSolution))
			print(cost(bestSolution))

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

			#time = timeit.default_timer() - start			
			timeDiff = time.time() - start

		T = annealingParameters.r*T


	pfp.printFloorplan(rectangles,'Output/annealing.png')
	return bestSolution



anneal(utils.benchmarks[0], annealingParameters,metrics.costArea)