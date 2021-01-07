import numpy as np
import struct
from array import array
from os.path import join
import random
import pandas as pd
import os
import sys
from classification_functions import MnistDataloader

def divideToClusters(arr, nrows, ncols):

    h, w = arr.shape
    assert h % nrows == 0, "{} rows is not evenly divisble by {}".format(h, nrows)
    assert w % ncols == 0, "{} cols is not evenly divisble by {}".format(w, ncols)
    return (arr.reshape(h//nrows, nrows, -1, ncols)
               .swapaxes(1,2)
               .reshape(-1, nrows, ncols))


if __name__ == "__main__":
	if (len(sys.argv) == 12):
		i = 0
		for var in sys.argv:										# get values from command line
			if (var == "-d"):
				input_original = sys.argv[i + 1]
			if (var == "-q"):
				queries_original = sys.argv[i + 1]
			if (var == "-l1"):
				labels_input = sys.argv[i + 1]
			if (var == "-l2"):
				labels_queries = sys.argv[i + 1]
			if (var == "-o"):
				output_file = sys.argv[i + 1]

			i = i + 1
	else:
		print("Wrong input. Using default values.")

		input_original = 'train-images-idx3-ubyte'  		# default values if not given by user
		queries_original = 't10k-images-idx3-ubyte'
		labels_input = 'train-labels-idx1-ubyte'
		labels_queries = 't10k-labels-idx1-ubyte'
		output_file = 'results_emd.txt'

	(xtrain, ytrain) = MnistDataloader(input_original, labels_input)	# read datasets
	(xtest, ytest) = MnistDataloader(queries_original, labels_queries)

	x_train = np.array(xtrain)
	x_test = np.array(xtest)
	y_train = np.array(ytrain)
	y_test = np.array(ytest)

	x_train = np.reshape(x_train, (len(x_train), 28, 28, 1))
	x_test = np.reshape(x_test, (len(x_test), 28, 28, 1))

	x_train2d = np.reshape(x_train, (len(x_train), 28, 28))
	x_test2d = np.reshape(x_test, (len(x_test), 28, 28))


	signatures_train = [[[0 for k in range(2)] for j in range(16)] for i in range(len(x_train2d))]
	i = 0
	for image in x_train2d:
		
		temp = divideToClusters(image, 7, 7)
		
		for j in range(16):
			signatures_train[i][j][1] = np.sum(temp[j])				# w
			signatures_train[i][j][0] = temp[j][3][3]				# p

		i += 1


	signatures_test = [[[0 for k in range(2)] for j in range(16)] for i in range(len(x_test2d))]
	i = 0
	for image in x_test2d:
		
		temp = divideToClusters(image, 7, 7)
		
		for j in range(16):
			signatures_test[i][j][1] = np.sum(temp[j])				# w
			signatures_test[i][j][0] = temp[j][3][3]				# p

		i += 1
