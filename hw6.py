'''
Grant Ikehara, Cameron Healy, Dominic Soares
HW #6
hw6.py
CPSC 310-01

'''

import csv
import sys
import math
import copy
import numpy
from tabulate import tabulate
import random

'''
The read_csv() function is the same function introduced in class. It returns a table
filled with the selected file's CSV data. It is used to open all files.
'''
def read_csv(filename):
	the_file = open(filename, 'r')
	the_reader = csv.reader(the_file, dialect='excel')
	table = []
	for row in the_reader:
		if len(row) > 0:
			table.append(row)
	the_file.close()
	return table

'''
Returns a random subset of size F from the input table 
'''
def random_attribute_subset(attributes, F):
	# shuffle and pick first F
	shuffled = attributes[:]  # make a copy
	random.shuffle(shuffled)
	return shuffled[:F]

'''
Returns the test and remainder sets for the random forest classifier 
'''
def generate_test_and_remainder(table):
	third_of_data = len(table)/3
	test = random_attribute_subset(table, third_of_data)
	remainder = random_attribute_subset(table, 2*third_of_data)
	return test, remainder

'''
returns the frequencis of all attributes in the instance set as a dictionary
'''
def attribute_frequencies(instances, att_index, class_index):
	att_vals = list(set(get_column(instances, att_index))) 
	class_vals = list(set(get_column(instances, class_index)))
	result = {v: [{c: 0 for c in class_vals}, 0] for v in att_vals}
	for row in instances:
		label = row[class_index]
		att_val = row[att_index]
		result[att_val][0][label] += 1
		result[att_val][1] += 1
	return result

'''
Calculates the E_new of the instance set and returns it
'''
def calc_enew(instances, att_index, class_index):
	D = len(instances)
	freqs = attribute_frequencies(instances, att_index, class_index)
	E_new = 0
	for att_val in freqs:
		D_j = float(freqs[att_val][1])
		probs = [(c/D_j) for (_, c) in freqs[att_val][0].items()]
		E_D_j = -sum([p*log(p,2) for p in probs])
		E_new += (D_j/D)*E_D_j
	return E_new 

'''
Returns the index of the attribute with the least entropy
'''
def pick_attribute(instances, att_indexes, class_index):
	ents = []
	for att_i in att_indexes:
		ents.append(calc_enew(instances, att_i, class_index))
	min_ent = ents.index(min(ents))
	return min_ent

'''
Creates a decision tree recursively
'''
def tdidt(instances, att_indexes, att_domains, class_index):
	if same_class(instances, class_index):
		return instances
	if len(instances) == 0:
		return instances
	min_ent = pick_attribute(instances, att_indexes, class_index)


'''
The main function
'''
def main():
	print "==========================================="
	print "STEP 1: "
	print "==========================================="
	table = read_csv('auto-data.txt')


if __name__ == '__main__':
	main()