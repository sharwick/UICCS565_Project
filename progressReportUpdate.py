from initializeMatchPairs import initializeMatchPairs
from annealer import anneal
import metrics
import alignImages
import classes
import utils

annealingParameters = classes.AnnealingParameters(100,.85,5,.05,1,1)

def analyzeAllBenchmarks():
	for dataset in utils.benchmarks:
		initializeMatchPairs(dataset)
		anneal(dataset, annealingParameters,metrics.costArea)
		alignImages.createImages('Output/initialMatchPairs_','Output/annealing_','Output/Comparison of Initial to Annealed_')

analyzeAllBenchmarks()