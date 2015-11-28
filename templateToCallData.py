import annealer
import classes
import metrics


dataset = 'ami33'

annealingParameters = classes.AnnealingParameters(100,.85,5,.05,1,1)
(root, rectangles, dictionary, matrix) = annealer.anneal(dataset, annealingParameters,metrics.costArea)

print(dictionary)