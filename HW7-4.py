'''
Grant Ikehara, Cameron Healy, Dominic Soares
HW #6
hw6.py
CPSC 310-01
Purpose:
    To implement an a priori rule miner as opposed to the decision trees
    and random forests that we've been mucking around with. We're really
    just printing out a mined ruleset and describing it.
Design Checklist:
    No steps this time, should be interesting. So here's your list:
    [] Create aPriori Algorithm. 
    For titanic Dataset:
        At various min support levels:
            [] implement algorithm, mine rules
            [] print rules
            [] describe rules, do they:
                [] make sense
                [] compare to HW4 and HW5
        [] Discuss how various min support and confidence affected this.
        
    For shroom Dataset:
        At various min support levels:
            [] implement algorithm, mine rules
            [] print rules
            [] describe rules, do they:
                [] make sense
                [] compare to HW4 and HW5
            [] Read the book so you know what feature selection is
            [] Do feature selection
        [] Discuss how various min support and confidence affected this.
        
    
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
from collections import Counter

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
As self-explanatory as it gets
'''
def getRidOfFirstLine(table): #Just for the titanic
    i = 0
    newtable = []
    for row in table:
        if i != 0:
            newtable.append(table[i])
        i +=1
    return newtable

'''
Gets a column in question.
'''
def get_column(table, ind): #parse all the data into different lists
    listylist = [] #               0
    i = 0            
    for row in table: #Get nice subdivisions
        listylist.append(table[i][ind])   
        i += 1
    i = 0
    return (listylist)#return all of the lists

'''
Returns the frequency of the itemset
'''
def get_itemset_freq(itemset, table):
    checks = len(itemset)
    counter = 0
    count_itemset = 0
    for row in table:
        for item in itemset:
            if item in row:
                counter += 1
        if counter == checks:
            count_itemset += 1
        counter = 0
    return count_itemset

'''
Returns the support of the itemset
'''
def get_support(itemset, table):
    count = get_itemset_freq(itemset, table)
    support = count/(len(table)*1.0)
    return support

'''
Returns the confidence of the itemset
'''
def get_confidence(itemset, table, LHS):
    count = get_itemset_freq(itemset, table)
    countL = get_itemset_freq(LHS, table)
    conf = count/(countL*1.0)
    return conf

'''
Returns the lift of the itemset

UNFINISHED
'''
def get_lift(itemset, table, LHS, RHS):
    supp = get_support(itemset, table)
    suppL = get_support(LHS, table)
    suppR = get_support(RHS, table)
    return (supp/(suppL*suppR))

'''
Returns the list of atts by column
'''
def get_col_atts(table, cols):
    ListOfAtts = []
    for i in range(cols):
        column = get_column(table, i)
        AttsInCol = []
        for item in column:
            if item not in AttsInCol:
                AttsInCol.append(item)
        ListOfAtts.append(AttsInCol)
    return ListOfAtts
            
def RHSandLHSok(RHS, LHS, ColsOfAtts):
    for listy in ColsOfAtts:
        if RHS in listy and LHS in listy:
            return False
    return True    

'''
A priori algorithm for titanic
'''
def apriori_titanic(table, min_supp, min_conf):
    ColsOfAtts = get_col_atts(table, 4)
    ListOfAtts = []
    for row in table:
        for item in row:
            if item not in ListOfAtts:
                ListOfAtts.append(item)
    ListOfRules = []
    i = 1
    for att1 in ListOfAtts:
        for att2 in ListOfAtts:
            support = get_support([att1, att2], table)
            conf = get_confidence([att1, att2], table, [att1])
            lift = get_lift([att1, att2], table, [att1], [att2])
            if RHSandLHSok(att1, att2, ColsOfAtts) and support >= min_supp and conf >= min_conf:
                ListOfRules.append([i, [att1], [att2], support, conf, lift])
                i += 1
    for row in ListOfRules:
        print row

'''
The main function
'''
def main():
    print "==========================================="
    print "STEP 1: "
    print "==========================================="
    table0 = read_csv('titanic.txt')
    table0 = getRidOfFirstLine(table0)

    table1 = read_csv('agaricus-lepiota.txt')
    apriori_titanic(table0, 0.1, 0.8)


if __name__ == '__main__':
    main()