# -*- coding: utf-8 -*-
#*****************************************#
# Assignment 1                            #
# Name: Keyur K Mehta                     #
# Apriori Algorithm                       #
#*****************************************#

from collections import Counter
import itertools
import math

# Open a file and save the transactions in the list
fileName = raw_input("Enter a file name to be read: ")
with open(fileName) as f:    #'test_data.dat' fileName
    datalist = []
    for line in f:
        data = []
        line = line.split()   # to deal with blank 
        if line:              
            #Convert string into numbers
            line = [int(i) for i in line]
            # to check duplicate in each line
            for num in line:
                if num not in data:
                    data.append(num)
            datalist.append(data)

print("The dataset is  read and saved to the list..")
length = len(datalist)
print("Total no of transaction in the file are:", length)
f.close()
print("===============================================================")

min_support_per = int(input("Enter the minimum support in percentage: "))
min_support = (min_support_per * length) / 100
print("The minimum support in terms of transaction is: ", min_support)
print("===============================================================")

counter = Counter(itertools.chain(*datalist))
item_set = list(counter.keys())
print("\n The elements of itemset in the file are:")
print(item_set)
    
print("\nThe frequency of each items is: ")
print(counter.elements)
print("===============================================================")

list_freq_itemset = []
freq_itemset_cnt = {}
for i in counter:
    if counter.get(i) >= min_support:
        freq_itemset_cnt.update({i:counter.get(i)})
print("\nThe frequent item set with its count in 1st iteration is: ", freq_itemset_cnt)
freq_itemset = list(freq_itemset_cnt.keys())
print("The keys are: ",freq_itemset)
list_freq_itemset.append(freq_itemset_cnt)
print("===============================================================")
    
def get_combinatins_items(item_set,k):
    item_set = list(itertools.combinations(item_set,k))
    print("The combinations item set in iteration", k, " are:")
    print(item_set)
    return item_set

def get_pruning(freq_itemset, k):
    print(k)
    temp3 = set()
    temp2 = set()
    temp3 = set(list_freq_itemset[k-1])
    print("temp3",temp3)
    prun_freq_itemset = []
    for i in freq_itemset:
        temp = set(list(itertools.combinations(i,k)))
        print(temp)
        c = 0
        for t in temp:
            temp2 = set(list(t))
            print("temo2",t)
            
            if t.issubset(temp3):
                print("inside")
                c +=1
        if c == len(temp):
            prun_freq_itemset.append(i)
            c=0
    print(prun_freq_itemset)
    
            
def get_freq_itemset(freq_itemset,datalist,min_support):
    freq_set = set(freq_itemset)
    freq_cnt = {}
    freq_itemset_cnt = {}
    for i in freq_set:
        temp = set(i)
        for t in datalist:
            temp2 = set(t)
            if temp.issubset(temp2):
                if i not in freq_cnt:
                    freq_cnt.update({i:1})
                else:
                    freq_cnt[i] = freq_cnt.get(i) + 1
    print("\nThe item set with its count are:")
    print(freq_cnt)
    nxt_freq_itemset = []
    for i in freq_cnt:
        if freq_cnt.get(i) >= min_support:
            nxt_freq_itemset.append(i)
            freq_itemset_cnt.update({i:freq_cnt.get(i)})
    print("\nThe frequent item set is:")
    
    if len(nxt_freq_itemset) != 0:
        list_freq_itemset.append(freq_itemset_cnt)
        print(nxt_freq_itemset)
    #else:
    #    list_freq_itemset.append(freq_cnt)
    #    print(freq_cnt.keys())
    return nxt_freq_itemset

k = 1
while len(freq_itemset) != 0:
    k +=1
    if k == 2:
        freq_itemset = list(set(itertools.chain(freq_itemset)))
    else:
        freq_itemset = list(set(itertools.chain.from_iterable(freq_itemset)))
    freq_itemset = get_combinatins_items(freq_itemset,k)
    #if k > 3:
    #    freq_itemset = get_pruning(freq_itemset,k-1)
    freq_itemset = get_freq_itemset(freq_itemset,datalist,min_support)
    print("===============================================================")

print("All the frequent Item set in the data are:")
print(list_freq_itemset)   
print("===============================================================")

print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("+++++++++++++++++Maximal and Closed Frequent Itemset+++++++++++++++++++")

print("Total Iterations: ",k)
print("All the frequent Item set in the data are:")
print(list_freq_itemset)

# Closed Frequent Itemset
closed_freq_set = []
for l in range(0,k-1):
    if l != k-2:
        curr_list = list_freq_itemset[l]
        curr_freq = set(curr_list.keys())
        curr_supp = set(curr_list.values())
        #print(l, curr_freq)
        next_list = list_freq_itemset[l+1]
        next_freq = set(next_list.keys())
        next_supp = set(next_list.values())
        for i in curr_freq:
            #print(i)
            if l ==0:
                temp = set(itertools.chain([i]))
            else:
                temp = set(itertools.chain.from_iterable([i]))
            temp2 = set()
            #print(temp)
            for j in next_freq:
                if temp.issubset(set(itertools.chain(j))):
                    #print("inside")
                    if curr_list.get(i) == next_list.get(j):
                        temp2.update([j])
            if len(temp2) == 0:
                #print("max", temp2)
                closed_freq_set.append(i)
    else:
        curr_list = list_freq_itemset[l]
        curr_freq = set(curr_list.keys())
        #print(l, curr_freq)
        for i in curr_freq:
            closed_freq_set.append(i)
print("\nThe Closed Frequent Itemset:")
print(closed_freq_set)        
print("===============================================================")

# Maximal Frequent Itemset
max_freq_set = []
for l in range(0,k-1):
    if l != k-2:
        curr_list = list_freq_itemset[l]
        curr_freq = set(curr_list.keys())
        #print(curr_freq)
        next_list = list_freq_itemset[l+1]
        next_freq = set(next_list.keys())
        for i in curr_freq:
            #print(i)
            if l ==0:
                temp = set(itertools.chain([i]))
            else:
                temp = set(itertools.chain.from_iterable([i]))
            temp2 = set()
            #print(temp)
            for j in next_freq:
                #print(set(itertools.chain(j)))
                if temp.issubset(set(itertools.chain(j))):
                    #print("inside")
                    temp2.update([j])
            if len(temp2) == 0:
                #print("max", temp2)
                max_freq_set.append(i)
    else:
        curr_list = list_freq_itemset[l]
        curr_freq = set(curr_list.keys())
        #print(curr_freq)
        for i in curr_freq:
            max_freq_set.append(i)
print("\nThe Maximal Frequent Itemset:")
print(max_freq_set)
print("===============================================================")

print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("++++++++++++++++++++++++++Association Rule+++++++++++++++++++++++++++++")

min_confidence = int(input("Enter the minimum confidence in percentage: "))
print("The minimum confidence in terms is: ", min_confidence)

print("All the frequent Item set in the data are:")
print((list_freq_itemset))
   
print("===============================================================")
rules = []
confidence = 0
all_confidence = 0
cosine = 0
st = ''
print("Total Iterations: ",k)
for l in range(1,k-1):
    curr_list = list_freq_itemset[l]
    curr_freq = set(curr_list.keys())
    print(curr_list)
    
    
    for i in curr_freq:
        if len(i) > 1:
            X =set(i)
            temp = set(itertools.chain.from_iterable([i]))
            #print(temp)
            temp2 = []
            for x in range(1,len(temp)+1):
                temp3 = list(itertools.chain(itertools.permutations(temp,x)))
                temp2.append(temp3)
            temp4 = set(list(itertools.chain.from_iterable(temp2)))
            for A in temp4:
                B = X.difference(A)
                
                if B:
                    AB = set(A) | B
                    t_list = list_freq_itemset[len(AB)-1]
                    b_list = list_freq_itemset[len(A)-1]
                    e_list = list_freq_itemset[len(B)-1]
                    ss= str(A)
                    if len(ss) == 4:
                        st = ss[1]
                    #print(AB,t_list.get(tuple(AB)), A, st, b_list.get(int(st)), next(iter(B)),e_list.get(next(iter(B))))
                    if len(ss) == 4:
                        try:
                            confidence = round((t_list.get(tuple(AB))/b_list.get(int(st))) * 100,2)
                            all_confidence = round((t_list.get(tuple(AB))/max(b_list.get(int(st)),e_list.get(tuple(B)))) * 100,2)
                            cosine = round((t_list.get(tuple(AB))/math.sqrt((b_list.get(int(st))*e_list.get(tuple(B))))) * 100,2)
                        except:
                            pass
                        #print(confidence)
                    else:
                        try:
                            confidence = round((t_list.get(tuple(AB))/b_list.get(tuple(A))) *100,2)
                            all_confidence = round((t_list.get(tuple(AB))/max(b_list.get(int(st)),t_list.get(tuple(B)))) * 100,2)
                            cosine = round((t_list.get(tuple(AB))/math.sqrt((b_list.get(int(st))*e_list.get(tuple(B))))) * 100,2)
                            #print(confidence)
                        except:
                            pass
                    if confidence >= min_confidence:
                        a_rule = {"A":A,"B":B,"Confidence":confidence,"all_confidence":all_confidence,"cosine":cosine}
                        rules.append(a_rule) 

print("The Association Rules with its parameters are:",rules)
print()







