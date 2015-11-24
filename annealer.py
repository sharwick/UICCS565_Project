########################################################################
#	Annealing algorithm based on class notes (L08_fp-fp2.pdf)
########################################################################

import utils
import timeit
import math
import random
import metrics
from initializeMatchPairs import initializeMatchPairs

annealingParameters = classes.AnnealingParameters(100,.85,5,.05,1000000,1)

def anneal(dataset, annealingParameters, cost):

	# Setup
	start = timeit.default_timer()
	initialSolution = initializeMatchPairs(dataset)

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
		MT = 1
		uphill = 0
		reject = 0

		time = timeit.default_timer() - start

		while (reject/MT <= 1-annealingParameters.thresholdAccepted) and T>=thresholdTime and time<=thresholdTime:
			newSolution = updateSolution(bestSolution)

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

		T = annealingParameters.r*T



anneal(utils.benchmarks[0], annealingParameters,metrics.costArea)