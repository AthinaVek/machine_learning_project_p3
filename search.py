import numpy as np
import struct
from array import array
from os.path import join
import random
import pandas as pd
import os
import sys
from classification_functions import MnistDataloader
from scipy.stats import wasserstein_distance
from sklearn.metrics.pairwise import manhattan_distances


class Pair:
	def __init__(self, x, y) -> None:
		self.index = x
		self.distance = y

	def __str__(self) -> str:
		return str(self.index) + " " + str(self.distance)

	def __repr__(self) -> str:
		return str(self.index) + " " + str(self.distance)


def manhattan_distance(p, q):
    return sum([abs(p[i]-q[i]) for i in range(len(p))])


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

	# x_train = np.reshape(x_train, (len(x_train), 28, 28, 1))
	# x_test = np.reshape(x_test, (len(x_test), 28, 28, 1))

	# x_train2d = np.reshape(x_train, (len(x_train), 28, 28))
	# x_test2d = np.reshape(x_test, (len(x_test), 28, 28))

	def f(pair):
		return pair.distance

	pVec_emd = []
	pVec_manhattan = []
	average_correct_emd = []
	average_correct_manhattan = []

	for q in range(len(x_test)):
		for i in range(len(x_train)):
			dist_emd = wasserstein_distance(x_test[q], x_train[i])
			pVec_emd.append(Pair(i, dist_emd))

			dist_manhattan = manhattan_distance(x_test[q], x_train[i])
			pVec_manhattan.append(Pair(i, dist_manhattan))

		pVec_emd.sort(key = f)
		pVec_manhattan.sort(key = f)

		correct_emd = 0
		correct_manhattan = 0
		for j in range(10):
			if (y_test[q] == y_train[pVec_emd[j].index]):
				correct_emd += 1
			if (y_test[q] == y_train[pVec_manhattan[j].index]):
				correct_manhattan += 1

		average_correct_emd.append(float(correct_emd)/10)
		average_correct_manhattan.append(float(pVec_manhattan)/10)

	average_emd = sum(average_correct_emd)
	average_manhattan = sum(average_correct_manhattan)
	print (average_emd)
	print (average_manhattan)
	
