########################################################################
# A single rect represents a module, along with geographic data
class Rect:
	def __init__(self,inX,inY,inW,inH,name):
		self.x = inX
		self.y = inY
		self.w = inW
		self.h = inH
		self.name = name

	def makePatch(self):
		p = patches.Rectangle(
				(self.x,self.y),
				self.w,
				self.h,
				hatch='/',
	        	fill=True,	   
	        	facecolor="#959595", 
			)
		return p
########################################################################