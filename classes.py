import matplotlib.pyplot as plt
import matplotlib.patches as patches

########################################################################
# A single rect represents a module, along with geographic data
class Rect:
	def __init__(self,inX,inY,inW,inH,name):
		self.x = inX
		self.y = inY
		self.w = inW
		self.h = inH
		self.name = name
		self.connections = 0
		self.connectionsRatio = 0

	def makePatch(self):
		p = patches.Rectangle(
				(self.x,self.y),
				self.w,
				self.h,
				#hatch='/',
	        	fill=True,	   
	        	facecolor="#959595", 
			)
		return p
########################################################################


class RectNode:
	def __init__(self,left,right,type,rect):
		self.left = left	# a RectNode or a Rect
		self.right = right	# a RectNode or a Rect
		self.type = type 	# "-" or "|" or "rect"
		self.rect = rect  	# if stack == "node" then this is a Rect object