import numpy as np
from copy import copy, deepcopy
from classes import RectNode, Rect

benchmarks = ["ami33", "ami49","apte", "hp", "xerox"] # To make performing operations on all benchmarks easier

# Return the indices of the maximum value of a matrix.  Don't return along diagonal unless there are no matches left.
def getMaxOfMatrix(matrix):
	maxValue = np.max(matrix)

	backup = -1

	for i in range(len(matrix)):
		for j in range(len(matrix)):
			if maxValue==matrix[i,j]:
				if i==j:
					backup = (i,j)
				else:
					return (i,j)

	return backup


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

	# Recursive calls - adjust the right branch with the dimensions of the left/bottom branch
	if root.left is not None:
		_updateTreeDimensionsHelper(root.left,wAdj,hAdj)

	if root.right is not None:
		wAdjSub = wAdj
		hAdjSub = hAdj

		if root.type == '|' and root.left is not None:
			wAdjSub += root.left.w

		if root.type == '-' and root.left is not None:
			hAdjSub += root.left.h

		_updateTreeDimensionsHelper(root.right,wAdjSub,hAdjSub)

	return True

# Reset all rectangles to origin
def resetRectangles(rectangles):
	for r in rectangles:
		r.x=0
		r.y=0
	return True


def sortByShape(node):
	# return node.h/node.w # aspect ratio made it worse
	# return node.w # width alone improved by 50%
	# return node.w*node.h # area made a bit worse but not like aspect ratio
	# return node.h # height improved but not as much as width
	return max(node.h,node.w)


# Consider the possible rotations of the rectangles and update the height/width/origin to represent minimal area pairing
# Can be used from rectangles or nodes
def optimizeTwoRectangles(rect1,rect2):
	# Need only rotate and/or move one rectangle (say rect2). 

	# Defaults (to be below later if necessary) 
	sign = "|"

	# Case 1 - no flip, above
	w = max(rect1.w,rect2.w)
	h = rect1.h + rect2.h
	area1 = w*h

	# Case 2 - no flip, aside
	w = rect1.w + rect2.w
	h = max(rect1.h,rect2.h)
	area2 = w*h

	# Case 3 - flip, above
	w = max(rect1.w,rect2.h)
	h = rect1.h + rect2.w
	area3 = w*h

	# Case 4 - flip, aside
	w = rect1.w + rect2.h
	h = max(rect1.h,rect2.w)
	area4 = w*h

	# Final area of the combo
	area = min(area1,area2,area3,area4)

	#print(str(isinstance(rect2,RectNode)) + '|' + str(isinstance(rect2,RectNode)))

	if area==area1:
		sign = "-"		
	elif area==area2:
		sign = "|"		
	elif area==area3:
		if isinstance(rect2,Rect):
			flipRect(rect2)
		else:
			flipNode(rect2)
		sign = "-"				
	else:
		if isinstance(rect2,Rect):
			flipRect(rect2)
		else:
			flipNode(rect2)
		sign = "|"

	def printTest():
		print(rect1.name + "|" + rect2.name)
		print((area1,area2,area3,area4))
		if sign=="|":
			print((rect1.w+rect2.w)*max(rect1.h,rect2.h))
		else:
			print((rect1.h+rect2.h)*max(rect1.w,rect2.w))

	return sign;


# Switch the height and width of a rectangle
def flipRect(rect):
	temp = rect.w
	rect.w = rect.h
	rect.h = temp
	rect.flipped = not rect.flipped
	return True

# Recursively flip all componenents of a node (subnodes/modules)
def flipNode(node):
	# Update top level dimensions
	temp = node.w
	node.w = node.h
	node.h = temp

	if node.type=='rect':
		flipRect(node.rect)
		return True
	elif node.type == '|':
		node.type = '-'
	else:
		node.type = '|'

	# Recursively update descendant nodes, including modules
	if node.left is not None:
		flipNode(node.left)
	if node.right is not None:
		flipNode(node.right)

	return True

# Obtain new list of rectangles from root (used for cost function)
def getRectanglesFromRoot(root):
	if root.type == 'rect':
		return [root.rect]

	rectangles = []

	if root.left is not None:
		rectangles += getRectanglesFromRoot(root.left)

	if root.right is not None:
		rectangles += getRectanglesFromRoot(root.right)

	return rectangles

