#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 13:23:50 2017

@author: caitlin
"""
####This file creates sendict, which contains the semantic space vectors


from datetime import datetime
startTime = datetime.now();
                        
import numpy as np
import nltk
import pickle

#location of SUBTL word frequency data
mostfreqfile = "./input/SUBTL_ge1.txt"

#load list of words from frequency filtered list
f2 = open(mostfreqfile,"r")

mostfreq = [];
with open(mostfreqfile) as f2:
    for line in f2:
        mostfreq.append(line.strip())

sendict = {}
masterlist= []
for line in open("./semspace/Top200K-d400.vec"):
    listWords = line.split(" ")
    #print(listWords)
    cleanlist = []
    for word in listWords:
        if word != "":
            cleanlist.append(word.strip()) 
            
    a = cleanlist.pop(0).lower()
    if a.isalpha() and\
                a not in set(nltk.corpus.stopwords.words('english')) and\
                            a in mostfreq:
        
        cleanlist = list(map(float, cleanlist))   
        cleanlist = np.array(cleanlist, dtype = float)

        sendict[a] = cleanlist
print (sendict)
pickle.dump(sendict, open("sendict.p", "wb"))

print("\r\n")
print("task complete --- total time:")
print(datetime.now()-startTime);
print("\r\n")

from sys import getsizeof
print(getsizeof(sendict))



