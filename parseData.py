import printFloorplan as pf

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

			rect = pf.Rect(x1,y1,max(x1,x2,x3,x4),max(y1,y2,y3,y4))
			rectangles.append(rect)

	# Transform blocks
	diagonalizeRectangles(rectangles)


	# Print rectangles
	pf.printFloorplan(rectangles,"Output/"+dataset+".png")


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


parseBlocks("ami33")
parseBlocks("ami49")
parseBlocks("apte")
parseBlocks("hp")
parseBlocks("xerox")