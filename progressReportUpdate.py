from initializeMatchPairs import initializeMatchPairs
from annealer import anneal
import metrics
import alignImages
import classes
import utils
import numpy as np

annealingParameters = classes.AnnealingParameters(100,.85,5,.05,1,1)


def analyzeAllBenchmarks():
	for dataset in utils.benchmarks:
		(root, rectangles, dictionary, matrix) = initializeMatchPairs(dataset)

		length = len(rectangles)
		costParameters = classes.CostParameters(np.ones((length,length)),0.5,2,matrix)

		# Curry cost function
		def newCost(inRoot):
			#return metrics.costWithLamdas(rectangles, costParameters)
			return metrics.costWithLamdasFromRoot(inRoot, costParameters)

		print(metrics.costWithLamdas(rectangles,costParameters))
		print(newCost(root))
		#print("Length of root rectangles = " + str(len(utils.getRectanglesFromRoot(root))))
		#return

		anneal(dataset, annealingParameters,newCost)

		alignImages.createImages('Output/initialMatchPairs_','Output/annealing_','Output/Comparison of Initial to Annealed (new cost)_')






analyzeAllBenchmarks()


def analyzeAllBenchmarksAreaOnly():
	for dataset in utils.benchmarks:
		(root, rectangles, dictionary, matrix) = initializeMatchPairs(dataset)
		anneal(dataset, annealingParameters,metrics.costArea)
		alignImages.createImages('Output/initialMatchPairs_','Output/annealing_','Output/Comparison of Initial to Annealed (area cost)_')

#analyzeAllBenchmarksAreaOnly()