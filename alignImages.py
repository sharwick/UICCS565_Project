import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import utils


prefix1 = 'Output/initialMatchPairs_'
prefix2 = 'Output/annealing_'


def createImages(prefix1,prefix2,outDescription):
	suffix = '.png'
	length = len(utils.benchmarks)
	images = []

	for i in range(length): #range(length):
		dataset = utils.benchmarks[i]

		img1 = mpimg.imread(prefix1+dataset+suffix)
		img2 = mpimg.imread(prefix2+dataset+suffix)

		fig = plt.figure(i)
		plt.subplot(1, 2,1)
		imgplot1 = plt.imshow(img1)
		plt.axis('off')

		#plt.subplot(1, 2,2*i+2)
		plt.subplot(1, 2,2)
		imgplot2 = plt.imshow(img2)
		plt.axis('off')

		fig.savefig(outDescription + dataset + '.png',dpi=100)
		#plt.show()

		plt.close('all')


#createImages(prefix1,prefix2)