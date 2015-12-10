from initializeMatchPairs import initializeMatchPairs
from annealer import anneal
import metrics
import alignImages
import classes
import utils
import numpy as np
from copy import copy, deepcopy
import random

#annealingParameters = classes.AnnealingParameters(100,.85,5,.05,1,1) # For testing
#annealingParameters = classes.AnnealingParameters(1000,.8,10,.01,1000,1) # For final
annealingParameters = classes.AnnealingParameters(5000,.8,10,.01,10000,1) # For final (longer run)

random.seed(1000) # Set seed so we can reproduce results

def analyzeAllBenchmarks():
	for dataset in utils.benchmarks:
		# Initial Floorplan
		(root, rectangles, dictionary, matrix) = initializeMatchPairs(dataset) 

		# Anneal - Consider area only
		anneal(dataset, annealingParameters,metrics.costArea,"Output/final_annealing_",'Annealed Floorplan - Area Only')  

		# Anneal - Consider area and connections
		length = len(rectangles)
		lambdas = copy(matrix)
		costParameters = classes.CostParameters(np.ones((length,length)),0.5,2,lambdas,dictionary)

		# Curry cost function
		def newCost(inRoot):
			#return metrics.costWithLamdas(rectangles, costParameters)
			return metrics.costWithLamdasFromRoot(inRoot, costParameters)


		anneal(dataset, annealingParameters,newCost,"Output/final_annealingNewCost_",'Annealed Floorplan - Area and Connections')


	alignImages.createImagesForFinal('Output/final_annealing_','Output/final_annealingNewCost_','Output/Final Comparison_')





analyzeAllBenchmarks()


def analyzeAllBenchmarksAreaOnly():
	for dataset in utils.benchmarks:
		(root, rectangles, dictionary, matrix) = initializeMatchPairs(dataset)
		anneal(dataset, annealingParameters,metrics.costArea)
		alignImages.createImages('Output/initialMatchPairs_','Output/annealing_','Output/Comparison of Initial to Annealed (area cost)_')

#analyzeAllBenchmarksAreaOnly()