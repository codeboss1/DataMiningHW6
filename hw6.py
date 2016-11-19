'''
Grant Ikehara, Cameron Healy, Dominic Soares
HW #6
hw6.py
CPSC 310-01

Purpose:
	To do the same thing we've been doing all semester, but use
	random forests as a classifier rather than the other characters we've seen
	so far.
Design Checklist:
	Contrary to the past few times, this round, not every step gets its own 
	function, especially given the fact that Step 1 wholly consists of 
	creating an algorithm without exactly implementing it.
	STEP 2:
	Upon Titanic Data:
		[] Get test set and remainder
		[] use bootstrapping to get 20 training and validation sets.
		[] create a decision tree for each of the above pairs F = 2.
		[] ALSO CREATE STANDARD D TREE
		[] get accuracy of each from the validation sets
		[] pick 7 best trees,
		[] apply those to test set, simple majority voting.
		[] get accuracy/error rate for RF
		[] make confusion matrix for RF
		[] get accuracy/error rate for simple tree
		[] make confusion matrix for simple tree
	Upon Auto Data:
		[] Get test set and remainder
		[] use bootstrapping to get 20 training and validation sets.
		[] create a decision tree for each of the above pairs F = 2.
		[] ALSO CREATE STANDARD D TREE
		[] get accuracy of each from the validation sets
		[] pick 7 best trees,
		[] apply those to test set, simple majority voting.
		[] get accuracy/error rate for RF
		[] make confusion matrix for RF
		[] get accuracy/error rate for simple tree
		[] make confusion matrix for simple tree
	STEP 3:
	Upon titanic data:
		Nice thing here is much here doesn't need to be hard-coded
		[] copy/paste the functions from Step 2 here.
		[] change N, M, and F to whatever we want.
		[] log the averages of the 5 runs with each setting.
		[] Find the one with the best accuracy.
		using those settings:
			[] print out accuracy/error rate
			[] print confusion matrix.
		[] Also output normal decision tree's accuracy and error rate
	Upon Auto Data:
		Nice thing here is much here doesn't need to be hard-coded
		[] copy/paste the functions from Step 2 here.
		[] change N, M, and F to whatever we want.
		[] log the averages of the 5 runs with each setting.
		[] Find the one with the best accuracy.
		using those settings:
			[] print out accuracy/error rate
			[] print confusion matrix.
		[] Also output normal decision tree's accuracy and error rate
	
		
	STEP 4:
	Upon Wisconsin.dat:
		List of attributes much longer now. 
		[] copy/paste the functions from Step 2 here
		[] change N, M, and F to whatever we want.
		[] log the averages of the 5 runs with each setting.
		[] Find the one with the best accuracy.
		using those settings:
			[] print out accuracy/error rate
			[] print confusion matrix.
		[] Also output normal decision tree's accuracy and error rate
		
	
Issues:
	TBD. 

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
Returns a list of pairs of training and validation sets. 
'''

def bootStrap(remainder, N): #Takes the big partition and bootstraps.
    """
    remainder: The table of instances not part of the test set.
    N: The number of total decision trees we want.
    """
    listOfTrainVal = []
    length = len(remainder)
    for i in range(N):
        twoPart = [[],[]]
        for j0 in range(length):
            inty = random.randrange(0,length)
            twoPart[0].append(remainder[inty])
        for j1 in range(length):
            isIn = 0
            for k0 in range(len(twoPart[0])):
                if remainder[j1] == twoPart[0][k0]:
                    isIn = 1
            if isIn == 0:
                twoPart[1].append(remainder[j1])
        listOfTrainVal.append(twoPart)
        
    
    return listOfTrainVal


'''
Gets discretized mpg rating
'''
def rate(x):   #Changes ratio mpg to ordinal mpg rating. I use this often.
    4
    
    y = 0
    if x <= 13.99999:
        y = 1
    elif x >= 14.0 and x < 15:
        y = 2
    elif x >= 15.0 and x < 17.0:
        y = 3
    elif x >= 17.0 and x < 20.0:
        y = 4
    elif x >= 20.0 and x < 24.0:
        y = 5
    elif x >= 24.0 and x < 27.0:
        y = 6
    elif x >= 27.0 and x < 31.0:
        y = 7
    elif x >= 31.0 and x < 37.0:
        y = 8
    elif x >= 37.0 and x < 45.0:
        y = 9
    elif x >= 45.0:
        y = 10
    return y


'''
Discretizes weight.
'''
def rateWeight(x): #Discretizes the weight into 5 categories
    if x <= 1999.999:
        y = 1
    elif x >= 2000 and x < 2500:
        y = 2
    elif x >= 2500 and x < 3000:
        y = 3
    elif x >= 3000 and x < 3500:
        y = 4
    elif x >= 3500:
        y = 5

    return y
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


def step2(inst0, inst1):
	pass
	
'''
The main function
'''
def main():
	print "==========================================="
	print "STEP 1: "
	print "==========================================="
	table0 = read_csv('auto-data.txt')
	table1 = read_csv('titanic.txt')
	table2 = read_csv('wisconsin.dat')
	print "Really nothing happens in Step 1. "
	print "We just built the classifier and then actually use in Step 2"
	print ""
	print ""
	print "==========================================="
	print "STEP 2: "
	print "==========================================="
	step2(table0, table1)
	step3(table0, table1)
	step4(table2)


if __name__ == '__main__':
	main()
