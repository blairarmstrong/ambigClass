#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 13:23:50 2017

@author: caitlin
"""
import numpy as np
import nltk

#location of SUBTL word frequency data
mostfreqfile = "./input/SUBTL_ge1.txt"

#load list of words from frequency filtered list
f2 = open(mostfreqfile,"r")

mostfreq = [];
with open(mostfreqfile) as f2:
    for line in f2:
        mostfreq.append(line.strip())


masterlist= []
for line in open("./semspace/semsample.txt"):
    listWords = line.split(" ")
    #print(listWords)
    cleanlist = []
    for word in listWords:
        if word != "":
            cleanlist.append(word.strip()) 
    #print(cleanlist)
    masterlist.append(cleanlist)
    print(len(cleanlist))
    
namelist= [] 
sendict = {}           
for cleanlist in masterlist:
    a = cleanlist.pop(0).lower()
    if a.isalpha() and\
                a not in set(nltk.corpus.stopwords.words('english')) and\
                            a in mostfreq:
        print(a)
    
        #print(namelist.append(a))
        #print(len(cleanlist))
        
        cleanlist = list(map(float, cleanlist))   
        #print(cleanlist)
        cleanlist = np.array(cleanlist, dtype = float)
        #print(cleanlist)
         #this puts it into numpy array format
    
        #d = {a:cleanlist}
        #print(d)
        sendict[a] = cleanlist
#print (sendict)





#then do for loop

#import csv
#reader = csv.reader(open("./semspace/semsample.txt"), delimiter=" ")
#for line in reader:
   # print(line)



