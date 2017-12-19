import numpy as np

def parse_to_matrix(filepath, separator = " "):
	"""
	By: Jan
	Reads a textfile to a matrix.
	Assumptions:Every line corresponds to one line of the matrix
	Every line has the same number of items

	separator is the sign with which weights are separated
	"""
	file = open(filepath, "r")

	array = []

	for line in file.readlines():
		weight_list = line.strip('\n').split(separator)
		array.append(weight_list)

	#return array
	return np.array(array, dtype = np.unicode_)