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

# Given a root, update the dimensions of the slicing tree to reflect the slicing tree
def updateTreeDimensions(root):
	_updateTreeDimensionsHelper(root,0,0)	

def _updateTreeDimensionsHelper(root,wAdj,hAdj):
	# Base case = node is a module
	if root.type == 'rect':
		root.rect.x += wAdj
		root.rect.y += hAdj
		return

	# Recursive calls
	_updateTreeDimensionsHelper(root.left,wAdj,hAdj)

	if root.right is not None:
		wAdjSub = wAdj
		hAdjSub = hAdj

		if root.type == '|' and root.left is not None:
			wAdjSub += root.left.w

		if root.type == '-' and root.left is not None:
			hAdjSub += root.left.h

		_updateTreeDimensionsHelper(root.right,wAdjSub,hAdjSub)

	return