import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import utils


prefix1 = 'Output/initialMatchPairs_'
prefix2 = 'Output/annealing_'
suffix = '.png'
length = len(utils.benchmarks)

images = []

#fig2, axes2 = plt.subplots(nrows=2*length,ncols=2)
#fig2.tight_layout() # prevents overlapping charts

#fig, axes = plt.subplots(nrows=1,ncols=2)
#fig.tight_layout()



for i in range(length): #range(length):
	dataset = utils.benchmarks[i]

	img1 = mpimg.imread(prefix1+dataset+suffix)
	img2 = mpimg.imread(prefix2+dataset+suffix)

	fig = plt.figure(i)
	
	#fig.axes.get_xaxis().set_visible(False)
	#fig.axes.get_yaxis().set_visible(False)
	plt.subplot(1, 2,1)
	imgplot1 = plt.imshow(img1)
	plt.axis('off')
	
	#plt.subplot(1, 2,2*i+2)
	plt.subplot(1, 2,2)
	imgplot2 = plt.imshow(img2)
	plt.axis('off')

	#plt.show()
	fig.savefig('Output/Comparison of Intial to Annealed_' + dataset + '.png',dpi=100)


def OLD():
	for i in range(1): #range(length):
		dataset = utils.benchmarks[i]

		img1 = mpimg.imread(prefix1+dataset+suffix)
		img2 = mpimg.imread(prefix2+dataset+suffix)

		plt.subplot(2*len(utils.benchmarks), 1,i+1)
		imgplot1 = plt.imshow(img1)

		plt.subplot(2*len(utils.benchmarks), 2,i+1)
		imgplot2 = plt.imshow(img2)


	plt.show()

	fig2.savefig('Output/test.png',dpi=100)

	#img = mpimg.imread(prefix1+utils.benchmarks[0]+suffix)
	#imgplot = plt.imshow(img)


plt.close('all')
