import annealer
import classes
import metrics
import numpy as np

dataset = 'ami33'

annealingParameters = classes.AnnealingParameters(100,.85,5,.05,1,1)
(root, rectangles, dictionary, matrix) = annealer.anneal(dataset, annealingParameters,metrics.costArea)

print(dictionary)

print("\n\nConnections Matrix\n\n")
print(matrix)




def costWithLamdas(rectangles, costParameters):
	dist_matrix = metrics.findMid(rectangles)
	#print(dist_matrix)

	matrix = costParameters.lamda
	leng = len(matrix)
	matrix_cost = np.zeros((leng,leng))
	for i in range(leng):
		for j in range(leng):
			matrix_cost[i][j]=(matrix[i][j]*dist_matrix[i][j])
	
	#print(matrix_cost)


	# Compute area based on new matrix
	area = 0

	return area
	
		
		
