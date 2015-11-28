import parseData as pd

rectangles = pd.createDiagonal('ami33')


#print(rectangles[0].name)
#print(rectangles[0].x)
#print(rectangles[0].y)
#print(rectangles[0].w)
#print(rectangles[0].h)
# Finding midpoints of rectangles
def findMid(rectangles):
	t = 0
	for r in rectangles:
		print('\n')
		midx1 = r.x + (r.w)/2
		midy1 = r.y + (r.h)/2
		#print (midx1,midy1)
		for j in rectangles:
			midx2 = j.x + (j.w)/2
			midy2 = j.y + (j.h)/2
			t+=1
			#print(midx2,midy2)
			d = abs(midx2 - midx1) + abs(midy2-midy1)	
			print d,
	print('\n')
	print(t)
	return (d)

	
	
def findMinX(rectangles):   
    minx = 10000000
    for r in rectangles:
        if(r.x < minx):
            minx = r.x
    return minx

def findMinY(rectangles):   
    miny = 10000000
    for r in rectangles:
        if(r.y < miny):
            miny = r.y
    return miny
    
def findMaxX(rectangles):   
    maxx = 0
    for r in rectangles:
        if(r.x > maxx):
            maxx = r.x + r.w
            
    return maxx

def findMaxY(rectangles):   
    maxy = 0
    for r in rectangles:
        if(r.y > maxy):
            maxy = r.y + r.h
            
    return maxy


<<<<<<< HEAD
   
def getAreaFloorplan(rectangles): # total area of floor
    MIN_X = findMinX(rectangles)
    MIN_Y = findMinY(rectangles)
    MAX_X = findMaxX(rectangles)
    MAX_Y = findMaxY(rectangles)
    top_fp_area = (MAX_X - MIN_X) * (MAX_Y - MIN_Y)
    print (top_fp_area)
    return 0

def getCoverage(rectangles): # sum of individual areas
    
    tot_area = 0
    
    for r in rectangles:
       print(r.name)
       area = r.w * r.h
       tot_area = tot_area + area 
       print(tot_area)      
    return tot_area

def getAreaRectangle(rectangleName): # rectangle name to rectangle area, need to call function "createDictionary" (in parseData)
	
    return 0


#print(getCoverage(rectangles))
#print(getAreaFloorplan(rectangles))
print(findMid(rectangles))

#print(manhattanDist(rectangles))
=======



#############################################################################
# Compute cost of a slicing tree based on overall area alone
def costArea(root):
	return root.w*root.h

>>>>>>> 9b480c0e3e32e7fea75c76e25b05d08f324dd108
