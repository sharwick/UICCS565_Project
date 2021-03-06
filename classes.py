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
		self.flipped = False		
		self.flag = False # Not used for a specific purpose.  Testing only.

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
	def printRect(self):
		print(self.name + '|' + str(self.x) + '|' + str(self.y) + '|' + str(self.w) + '|' + str(self.h) + '|' + str(self.flipped))

	def getArea(self):
		return self.w*self.h


########################################################################


class RectNode:
	def __init__(self,left,right,type,rect):
		self.left = left	# a RectNode or a Rect
		self.right = right	# a RectNode or a Rect
		self.type = type 	# "-" or "|" or "rect"
		self.rect = rect  	# if stack == "node" then this is a Rect object
		self.parent = None
		self.w = None
		self.h = None
		#self.whiteAspect = 0
		self.whiteArea = 0
		self.whiteLength = 0
		self.fitRect = None

		if type=='rect':
			self.w = self.rect.w
			self.h = self.rect.h

		else:
			# capture dimensions and parent structure
			wL = 0
			wR = 0
			hL = 0
			hR = 0

			if left is not None:
				left.parent = self
				wL = left.w
				hL = left.h
			if right is not None:
				right.parent = self
				wR = right.w
				hR = right.h

			if type=='|':
				self.w = wL+wR
				self.h = max(hL,hR)

				if (hL>=hR):
					self.whiteArea = wR*(hL-hR)
					self.whiteLength = max(wR,hL-hR)
				else:
					self.whiteArea = wL*(hR-hL)
					self.whiteLength = max(wL,hR-hL)
				

			if type=='-':
				self.w = max(wL,wR)
				self.h = hL+hR

				if (wL>=wR):
					self.whiteArea = hR*(wL-wR)
					self.whiteLength = max(hR,wL-wR)
				else:
					self.whiteArea = hL*(wR-wL)
					self.whiteLength = max(hL,wR-wL)

			
	def getArea(self):
		if self.w is not None and self.h is not None:
			return self.w*self.h
		return -1



########################################################################
class AnnealingParameters:
	# T = initial temp
	# r = adjustment to T
	# k = # of moves
	# thresholdAccepted = min percent of accepted moves
	# thresholdTime = max amount of time
	# thresholdTemp
	def __init__(self,T,r,k,thresholdAccepted,thresholdTime,thresholdTemp):
		self.T = T
		self.r = r
		self.k = k
		self.thresholdAccepted = thresholdAccepted
		self.thresholdTime = thresholdTime #(in microseconds)
		self.thresholdTemp = thresholdTemp
		return  
		

class CostParameters:
	# lamda = number of connections between two modules i and j
	# f = parameter measuring frequency of communication between two modules i and j
	# alpha = weight added to area

	def __init__(self,f,alpha,k,lamda,dictionary):
		self.lamda = lamda
		self.f = f 
		self.alpha = alpha
		self.k = k
		self.dictionary = dictionary
		return 
	

