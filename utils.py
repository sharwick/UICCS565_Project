import numpy as np

def getMaxOfMatrix(matrix):
	maxValue = np.max(matrix)

	for i in range(len(matrix)):
		for j in range(len(matrix)):
			if maxValue==matrix[i,j]:
				return (i,j)

	return -1


def getPolish(root):
	if root.type == 'rect':
		return '\n'+root.rect.name

	polish = ''
	if (root.left is not None):
		polish += getPolish(root.left)
	if (root.right is not None):
		polish += getPolish(root.right)

	polish += '\n'+root.type


	return polish