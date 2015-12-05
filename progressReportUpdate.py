from initializeMatchPairs import initializeMatchPairs
from annealer import anneal
import metrics
import alignImages
import classes
import utils
import numpy as np
from copy import copy, deepcopy

annealingParameters = classes.AnnealingParameters(100,.85,5,.05,1,1)


def analyzeAllBenchmarks():
	for dataset in utils.benchmarks:
		# Initial Floorplan
		(root, rectangles, dictionary, matrix) = initializeMatchPairs(dataset) 

		# Anneal - Consider area only
		anneal(dataset, annealingParameters,metrics.costArea,"Output/annealing_",'Annealed Floorplan - Area Only')  

		# Anneal - Consider area and connections
		length = len(rectangles)
		lambdas = copy(matrix)
		costParameters = classes.CostParameters(np.ones((length,length)),0.5,1,lambdas,dictionary)

		# Curry cost function
		def newCost(inRoot):
			#return metrics.costWithLamdas(rectangles, costParameters)
			return metrics.costWithLamdasFromRoot(inRoot, costParameters)


		anneal(dataset, annealingParameters,newCost,"Output/annealingNewCost_",'Annealed Floorplan - Area and Connections')

	alignImages.createImages('Output/initialMatchPairs_','Output/annealing_','Output/annealingNewCost_','Output/Comparison of Initial to Annealed (Area and All)_')






analyzeAllBenchmarks()


def analyzeAllBenchmarksAreaOnly():
	for dataset in utils.benchmarks:
		(root, rectangles, dictionary, matrix) = initializeMatchPairs(dataset)
		anneal(dataset, annealingParameters,metrics.costArea)
		alignImages.createImages('Output/initialMatchPairs_','Output/annealing_','Output/Comparison of Initial to Annealed (area cost)_')

#analyzeAllBenchmarksAreaOnly()