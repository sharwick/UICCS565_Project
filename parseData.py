import printFloorplan as pf
import numpy as np

datasets = ["ami33", "ami49","apte", "hp", "xerox"] # To make performing operations on all benchmarks easier


################################################################################################
# FUNCTIONS TO PARSE DATA


# Get block data from raw file
# Input = the name of a raw dataset (without file extension or directory)
# Output = a floorplan in the form of an array of rectangles
def parseBlocks(dataset):
	file = open("Data/"+dataset+".blocks",'r')

	rectangles = []
	
	# Extract corners and translate them into rectangles base on {lower left corner (x,y), width, height}
	for line in file:
		if line.find("hardrectilinear")>-1:
			
			subline = line[(line.find("(0")):]
			x1, y1, x2, y2, x3, y3, x4, y4 = (int(x.strip("(),")) for x in subline.split())

			#print(line) #check
			#print(subline) #check
			#print(x1+x2+x3+x4) # check
			#print(y1+y2+y3+y4) # check
			name = line.split()[0]

			rect = pf.Rect(x1,y1,max(x1,x2,x3,x4),max(y1,y2,y3,y4),name)
			rectangles.append(rect)

	return rectangles



# Get netlist data from raw file
# Input = the name of a raw dataset (without file extension or directory)
# Output = netlist data
def parseNetlists(dataset):
	file = open("Data/"+dataset+".nets",'r')
	netlists = []
	current = []

	for line in file:
		if line.find("NetDegree")>-1:
			if (len(current)>0):
				netlists.append(current)
				current = []

		elif line.find("%")>-1:
			current.append(line.split()[0])
	return netlists

# Capture the number of connections between modules
def createConnectionMatrix(netlists, dictionary):
	length = len(dictionary)
	matrix = np.zeros((length,length))

	for net in netlists:
		for i in net:
			for j in net:
				#print(i + "|" + j)
				if dictionary[i]!=dictionary[j]:
					matrix[dictionary[i],dictionary[j]] += 1

	return matrix

def createDictionary(rectangles):
	keys = []

	for r in rectangles:
		keys.append(r.name)

	d = dict.fromkeys(keys)

	for i in range(len(keys)):
		d[keys[i]] = i

	return d
	

################################################################################################
# FUNCTIONS TO CREATE IMAGES USING DESIRED ALGORITHMS

# Create an image of the given dataset using the diagonalize algorithm
# Input = the name of a raw dataset (without file extension or directory)
# Output = a .png saved in the Output directory.  No value is returned.
def printDiagonal(dataset):
	rectangles = parseBlocks(dataset)

	# Transform blocks
	diagonalizeRectangles(rectangles)

	# Print rectangles
	pf.printFloorplan(rectangles,"Output/"+dataset+".png")
	return

################################################################################################
# ALGORITHMS TO TRANSFORM FLOORPLANS


# Primitive algorithm to place blocks along diagonal (for testing)
def diagonalizeRectangles(rectangles):
	sumX = 0
	sumY = 0
	for r in rectangles:
		r.x = sumX
		sumX += r.w
		r.y = sumY
		sumY += r.h
	return

################################################################################################
# RUN ANALYSES ON ALL AVAILABLE DATASETS

def diagonalTest():
	for ds in datasets:
		printDiagonal(ds)

#diagonalTest()


def check(ds):
	rectangles = parseBlocks(ds)
	netlists = parseNetlists(ds)
	dictionary = createDictionary(rectangles)
	matrix = createConnectionMatrix(netlists,dictionary)


	def printChecks():
		print("Netlists")
		print(netlists)
		print("Dictionary")
		print(dictionary)
		print("Matrix:")
		print(matrix)
	#printChecks()

check('ami33')
#tag test
#tag SH TEST


