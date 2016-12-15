'''
Grant Ikehara, Cameron Healy, Dominic Soares
HW #7
hw7.py
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
            [X] implement algorithm, mine rules
            [X] print rules
            [X] describe rules, do they:
                [X] make sense
                [X] compare to HW4 and HW5
        [X] Discuss how various min support and confidence affected this.
        
    For shroom Dataset:
        At various min support levels:
            [X] implement algorithm, mine rules
            [X] print rules
            [X] describe rules, do they:
                [X] make sense
                [X] compare to HW4 and HW5
            [X] Read the book so you know what feature selection is
            [X] Do feature selection
        [X] Discuss how various min support and confidence affected this.
          
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
    if countL != 0:
        conf = count/(countL*1.0)
        return conf
    else:
        return 0

'''
Returns the lift of the itemset
'''
def get_lift(itemset, table, LHS, RHS):
    supp = get_support(itemset, table)
    suppL = get_support(LHS, table)
    suppR = get_support(RHS, table)
    if suppR*suppL != 0:
        return (supp/(suppL*suppR))
    else:
        return 0

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

'''
Ensures RHS and LHS are not of the same attribute
'''
def RHSandLHSok(RHS, LHS, ColsOfAtts):
    for listy in ColsOfAtts:
        for val1 in RHS:
            for val2 in LHS:
                if val1 in listy and val2 in listy:
                    return False
    return True  

'''
returns k-1 subsemt of itemset 
'''
def k_1_subsets(itemset):
      n = len(itemset)
      return [itemset[:i]+itemset[i+1:] for i in range(n)]

'''
returns L-k from C-k (a priori algo)
'''
def get_Lk_from_Ck(Ck1, min_supp, ColsOfAtts, table):
    Ck = []
    for A in Ck1:
        for B in Ck1:
            if A[0:-1] == B[0:-1] and A != B:
                mark = 1
                for subset in k_1_subsets(list(set().union(A,B))):
                    if subset not in Ck1:
                        mark = 0
                        break
                if mark == 1:
                    Ck.append(list(set().union(A,B)))
    Lk = []
    for item in Ck:
        if get_support(item, table) >= min_supp and item not in Lk:
            Lk.append(item)
    return Lk

'''
A priori algorithm for titanic
'''
def apriori_titanic(table, min_supp, min_conf):
    ColsOfAtts = get_col_atts(table, 4) #Sorts attribute values by attribute
    ListOfAtts = []
    for row in table:       #Creates list of un ordered attributes
        for item in row:
            if [item] not in ListOfAtts:
                ListOfAtts.append([item])
    FinalItemset = []
    for Att in ListOfAtts:  #Adds attributes that meet min_supp to new L1
        if get_support(Att, table) >= min_supp:
            FinalItemset.append(Att)
    Lnext = FinalItemset
    while len(Lnext) != 0:  #Creates Ln lists of supportd attribute itemsets 
        Lnext = get_Lk_from_Ck(Lnext, min_supp, ColsOfAtts, table)
        for val in Lnext:
            FinalItemset.append(val)
    for item1 in FinalItemset:
        for item2 in FinalItemset:
            if set(item2) == set(item1) and item1 != item2:
                FinalItemset.remove(item1)
                break
    ListOfRules = []
    i = 1
    for LHS in FinalItemset:   #Creates list of rules from supported itemsets
        for RHS in FinalItemset:
            support = get_support(LHS+RHS, table)
            conf = get_confidence(LHS+RHS, table, LHS)
            if RHSandLHSok(LHS, RHS, ColsOfAtts) and support >= min_supp and conf >= min_conf:
                newLHS = []
                newRHS = []
                for att1 in LHS:
                    for i in range(len(ColsOfAtts)):
                        if att1 in ColsOfAtts[i]:
                            newLHS.append([att1, i])
                            break
                for att2 in RHS:
                    for j in range(len(ColsOfAtts)):
                        if att2 in ColsOfAtts[j]:
                            newRHS.append([att2, j])
                            break
                ListOfRules.append([newLHS, newRHS])
                i += 1
    return ListOfRules


'''
A priori algorithm for mushrooms
'''
def apriori_mushrooms(table, min_supp, min_conf, num_cols):
    ColsOfAtts = get_col_atts(table, num_cols) #Sorts attribute values by attribute
    ListOfAtts = []
    for row in table:       #Creates list of un ordered attributes
        for item in row:
            if [item] not in ListOfAtts:
                ListOfAtts.append([item])
    FinalItemset = []
    for Att in ListOfAtts:  #Adds attributes that meet min_supp to new L1
        if get_support(Att, table) >= min_supp:
            FinalItemset.append(Att)
    Lnext = FinalItemset
    while len(Lnext) != 0:  #Creates Ln lists of supportd attribute itemsets 
        Lnext = get_Lk_from_Ck(Lnext, min_supp, ColsOfAtts, table)
        for val in Lnext:
            FinalItemset.append(val)
    for item1 in FinalItemset:
        for item2 in FinalItemset:
            if set(item2) == set(item1) and item1 != item2:
                FinalItemset.remove(item1)
                break
    ListOfRules = []
    i = 1
    for LHS in FinalItemset:   #Creates list of rules from supported itemsets
        for RHS in FinalItemset:
            support = get_support(LHS+RHS, table)
            conf = get_confidence(LHS+RHS, table, LHS)
            if RHSandLHSok(LHS, RHS, ColsOfAtts) and support >= min_supp and conf >= min_conf:
                newLHS = []
                newRHS = []
                for att1 in LHS:
                    for i in range(len(ColsOfAtts)):
                        if att1 in ColsOfAtts[i]:
                            newLHS.append([att1, i])
                            break
                for att2 in RHS:
                    for j in range(len(ColsOfAtts)):
                        if att2 in ColsOfAtts[j]:
                            newRHS.append([att2, j])
                            break
                ListOfRules.append([newLHS, newRHS])
                i += 1
    return ListOfRules

'''
Function to get stuff proper
'''
def tabulateCorrectly(listy,table):
    newStruct = []
    for i in range(len(listy)):
        newStructA = []
        s = ""
        newStructA.append(i+1)
        
        for j in range(len(listy[i][0])):
            if listy[i][0][j][1] == 0:
                s += "class: " + listy[i][0][j][0] + "    "
            elif listy[i][0][j][1] == 1:
                s += "age: " + listy[i][0][j][0] + "    "
            elif listy[i][0][j][1] == 2:
                s += "sex: " + listy[i][0][j][0] + "    "
            else:
                s += "survived: " + listy[i][0][j][0] + "    "
        newStructA.append(s)
        y = ""
        for j2 in range(len(listy[i][1])):
            if listy[i][1][j2][1] == 0:
                y += "class: " + listy[i][1][j2][0] + "    "
            elif listy[i][1][j2][1] == 1:
                y += "age: " + listy[i][1][j2][0] + "    "
            elif listy[i][1][j2][1] == 2:
                y += "sex: " + listy[i][1][j2][0] + "    "
            else:
                y += "survived: " + listy[i][1][j2][0] + "    "
        newStructA.append(y)
        newStructA.append(newSupport(listy[i],table))
        newStructA.append(newConf(listy[i],table))
        newStructA.append(newLift(listy[i],table))
        #append other things here
        newStruct.append(newStructA)
        
        
    print tabulate(newStruct, headers = ['LHS', 'RHS', 'Support', 'Confidence', 'Lift'])


'''
Function to get stuff proper
'''
def tabulateCorrectlyS(listy,table):
    newStruct = []
    for i in range(len(listy)):
        newStructA = []
        s = ""
        newStructA.append(i+1)
        for j in range(len(listy[i][0])):
            if listy[i][0][j][1] == 0:
                s += "Label: " + listy[i][0][j][0] + "    "
            elif listy[i][0][j][1] == 1:
                s += "CapShape: " + listy[i][0][j][0] + "    "
            elif listy[i][0][j][1] == 2:
                s += "CapSurface: " + listy[i][0][j][0] + "    "
            elif listy[i][0][j][1] == 3:
                s += "CapColor: " + listy[i][0][j][0] + "    "
            elif listy[i][0][j][1] == 4:
                s += "Bruises: " + listy[i][0][j][0] + "    "
            elif listy[i][0][j][1] == 5:
                s += "Odor: " + listy[i][0][j][0] + "    "
            elif listy[i][0][j][1] == 6:
                s += "gillA: " + listy[i][0][j][0] + "    "
            elif listy[i][0][j][1] == 7:
                s += "gillSp: " + listy[i][0][j][0] + "    "
            elif listy[i][0][j][1] == 8:
                s += "gillSi: " + listy[i][0][j][0] + "    "
            elif listy[i][0][j][1] == 9:
                s += "gillCo: " + listy[i][0][j][0] + "    "
            elif listy[i][0][j][1] == 10:
                s += "stalkSh: " + listy[i][0][j][0] + "    "
            elif listy[i][0][j][1] == 11:
                s += "stalkRo: " + listy[i][0][j][0] + "    "
            elif listy[i][0][j][1] == 12:
                s += "ssar: " + listy[i][0][j][0] + "    "
            elif listy[i][0][j][1] == 13:
                s += "ssbr: " + listy[i][0][j][0] + "    "
            elif listy[i][0][j][1] == 14:
                s += "scar: " + listy[i][0][j][0] + "    "
            elif listy[i][0][j][1] == 15:
                s += "scbr: " + listy[i][0][j][0] + "    "
            elif listy[i][0][j][1] == 16:
                s += "veilType: " + listy[i][0][j][0] + "    "
            elif listy[i][0][j][1] == 17:
                s += "veilColor: " + listy[i][0][j][0] + "    "
            elif listy[i][0][j][1] == 18:
                s += "ringNumber: " + listy[i][0][j][0] + "    "
            elif listy[i][0][j][1] == 19:
                s += "ringType: " + listy[i][0][j][0] + "    "
            elif listy[i][0][j][1] == 20:
                s += "spc: " + listy[i][0][j][0] + "    "
            elif listy[i][0][j][1] == 21:
                s += "pop: " + listy[i][0][j][0] + "    "
            elif listy[i][0][j][1] == 22:
                s += "habitat: " + listy[i][0][j][0] + "    "
        

        newStructA.append(s)
        y = ""
        for j2 in range(len(listy[i][1])):
            if listy[i][1][j2][1] == 0:
                y += "Label: " + listy[i][1][j2][0] + "    "
            elif listy[i][1][j2][1] == 1:
                y += "CapShape: " + listy[i][1][j2][0] + "    "
            elif listy[i][1][j2][1] == 2:
                y += "CapSurface: " + listy[i][1][j2][0] + "    "
            elif listy[i][1][j2][1] == 3:
                y += "CapColor: " + listy[i][1][j2][0] + "    "
            elif listy[i][1][j2][1] == 4:
                y += "Bruises: " + listy[i][1][j2][0] + "    "
            elif listy[i][1][j2][1] == 5:
                y += "Odor: " + listy[i][1][j2][0] + "    "
            elif listy[i][1][j2][1] == 6:
                y += "gillA: " + listy[i][1][j2][0] + "    "
            elif listy[i][1][j2][1] == 7:
                y += "gillSp: " + listy[i][1][j2][0] + "    "
            elif listy[i][1][j2][1] == 8:
                y += "gillSi: " + listy[i][1][j2][0] + "    "
            elif listy[i][1][j2][1] == 9:
                y += "gillCo: " + listy[i][1][j2][0] + "    "
            elif listy[i][1][j2][1] == 10:
                y += "stalkSh: " + listy[i][1][j2][0] + "    "
            elif listy[i][1][j2][1] == 11:
                y += "stalkRo: " + listy[i][1][j2][0] + "    "
            elif listy[i][1][j2][1] == 12:
                y += "ssar: " + listy[i][1][j2][0] + "    "
            elif listy[i][1][j2][1] == 13:
                y += "ssbr: " + listy[i][1][j2][0] + "    "
            elif listy[i][1][j2][1] == 14:
                y += "scar: " + listy[i][1][j2][0] + "    "
            elif listy[i][1][j2][1] == 15:
                y += "scbr: " + listy[i][1][j2][0] + "    "
            elif listy[i][1][j2][1] == 16:
                y += "veilType: " + listy[i][1][j2][0] + "    "
            elif listy[i][1][j2][1] == 17:
                y += "veilColor: " + listy[i][1][j2][0] + "    "
            elif listy[i][1][j2][1] == 18:
                y += "ringNumber: " + listy[i][1][j2][0] + "    "
            elif listy[i][1][j2][1] == 19:
                y += "ringType: " + listy[i][1][j2][0] + "    "
            elif listy[i][1][j2][1] == 20:
                y += "spc: " + listy[i][1][j2][0] + "    "
            elif listy[i][1][j2][1] == 21:
                y += "pop: " + listy[i][1][j2][0] + "    "
            elif listy[i][1][j2][1] == 22:
                y += "habitat: " + listy[i][1][j2][0] + "    "
        newStructA.append(y)
        newStructA.append(newSupport(listy[i],table))
        newStructA.append(newConf(listy[i],table))
        newStructA.append(newLift(listy[i],table))
        #append other things here
        newStruct.append(newStructA)
        
        
        
    print tabulate(newStruct, headers = ['LHS', 'RHS', 'Support', 'Confidence', 'Lift'])

'''
rewritten Support for data structure
'''
def newSupport(inst, table):
    itemSet = []
    for i in range(len(inst[0])):
        itemSet.append(inst[0][i][0])
    for i2 in range(len(inst[1])):
        itemSet.append(inst[1][i2][0])
    x = get_support(itemSet, table)
    return x

'''
rewritten Confidence for data structure
'''
def newConf(inst, table):
    itemSet = []
    LHS = []
    for i in range(len(inst[0])):
        itemSet.append(inst[0][i][0])
        LHS.append(inst[0][i][0])
        
    for i2 in range(len(inst[1])):
        itemSet.append(inst[1][i2][0])
    x = get_confidence(itemSet, table, LHS)
    return x

'''
rewritten Confidence for data structure
'''
def newLift(inst, table):
    itemSet = []
    LHS = []
    RHS = []
    for i in range(len(inst[0])):
        itemSet.append(inst[0][i][0])
        LHS.append(inst[0][i][0])
        
    for i2 in range(len(inst[1])):
        itemSet.append(inst[1][i2][0])
        RHS.append(inst[1][i2][0])
    x = get_lift(itemSet, table, LHS, RHS)
    return x

'''
Cuts down on the size of the mushroom dataset
'''
def rewriteTable(table): #Foregoes the whole auto-data table,
    #Instead just uses a truncated table with 4 rows, easy format.
    newTable = []
    for i in range(len(table)):
        row = []
        row.append(table[i][1]) 
        row.append(table[i][4]) 
        row.append(table[i][6]) 
        row.append(table[i][0]) 
        newTable.append(row)
    return newTable

'''
The main function
'''
def main():
    print "==========================================="
    print "Titanic"
    print "==========================================="
    table0 = read_csv('titanic.txt')
    table0 = getRidOfFirstLine(table0)
    rules0 = apriori_titanic(table0, 0.25, 0.75)
    tabulateCorrectly(rules0,table0)

    print "==========================================="
    print "Agaricus lepiota"
    print "==========================================="
    table1 = read_csv('agaricus-lepiota.txt')
    rules1 = apriori_mushrooms(table1, 0.75, 0.75, 23)
    tabulateCorrectlyS(rules1,table1)


if __name__ == '__main__':
    main()