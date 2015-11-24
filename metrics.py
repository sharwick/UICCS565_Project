import parseData as pd

rectangles = pd.createDiagonal('ami33')

print(rectangles[0].name)

def getAreaFloorplan(rectangles):
	return 0

def getCoverage(rectangles):
	return 0

def getAreaRectangle(rectangleName):
	return 0


print(getAreaFloorplan(rectangles))




#############################################################################
# Compute cost of a slicing tree based on overall area alone
def costArea(root):
	return root.w*root.h

