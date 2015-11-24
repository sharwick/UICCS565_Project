import numpy as np
from copy import copy, deepcopy
from classes import RectNode, Rect

benchmarks = ["ami33", "ami49","apte", "hp", "xerox"] # To make performing operations on all benchmarks easier

# Return the indices of the maximum value of a matrix
def getMaxOfMatrix(matrix):
	maxValue = np.max(matrix)

	for i in range(len(matrix)):
		for j in range(len(matrix)):
			if maxValue==matrix[i,j]:
				return (i,j)

	return -1


# Returns a string with Polish expression of a slicing tree
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

# Return an array version of the Polish expression (easier to manipulate than a string)
def getPolishArray(root):
	if root.type == 'rect':
		return [root.rect.name]

	polish = []
	if (root.left is not None):
		polish += getPolishArray(root.left)

	if (root.right is not None):
		polish += getPolishArray(root.right)

	polish += [root.type]

	return polish

# Construct a tree from Polish expression
def getTreeFromPolishArray(array, rectangles,dictionary):
	# Construct new tree
	stack = []

	for i in range(len(array)):
		element = array[i]

		# Create deep copy of rectangles when adding them to stack
		if element != '-' and element != '|':
			index = dictionary[element]
			newNode = RectNode(None,None,'rect',deepcopy(rectangles[dictionary[element]]))

			# Restart at 0 so I can rebuild given the new tree structure
			newNode.rect.x = 0
			newNode.rect.y = 0
			stack.append(newNode)
		else:
			right = stack.pop()
			left = stack.pop()
			newNode = RectNode(left,right,element,None)
			stack.append(newNode)

	# Get new dimensions
	root = stack[0]
	updateTreeDimensions(root)

	return root



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


def sortByShape(node):
	# return node.h/node.w # aspect ratio made it worse
	# return node.w # width alone improved by 50%
	# return node.w*node.h # area made a bit worse but not like aspect ratio
	# return node.h # height improved but not as much as width
	return max(node.h,node.w)
