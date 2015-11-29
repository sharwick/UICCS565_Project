import annealer
import classes
import metrics 
import numpy as np

dataset = 'ami33'

annealingParameters = classes.AnnealingParameters(100,.85,5,.05,1,1)
(root, rectangles, dictionary, matrix) = annealer.anneal(dataset, annealingParameters,metrics.costArea)

#print(dictionary)

#print("\n\nConnections Matrix\n\n")
#print(matrix)

f = np.zeros((len(rectangles),len(rectangles)))

for i in range (len(rectangles)):
	for j in range (len(rectangles)):
		f[i][j] = 1
		#print f[i][j],
	#print ('\n')
#print(rectangles[0].x)
costParameters = classes.CostParameters(f,0.75,1,matrix)
final_cost = metrics.costWithLamdas(rectangles, costParameters)
print final_cost
	
		
		
