#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 13:47:13 2017

@author: caitlin, blair

This module computes similarities between the individual vectors in the corpus
and between those extracted from the dictionary.  

"""

from datetime import datetime
startTime = datetime.now();

import pickle
import numpy as np
import math
import os.path
from scipy.stats.stats import pearsonr

def square_rooted(x):
    return (math.sqrt(sum([a*a for a in x])))

def cosine_similarity(x,y):
    numerator = sum(a*b for a,b in zip(x,y))
    denominator = square_rooted(x)*square_rooted(y)
    return (numerator/float(denominator))

#### USER SET VARIABLES #######################################################

#Import dictionary vectors from pickled file (defsspace)
defsspace = pickle.load(open("./eDom_filter/defsspace/defsspace.p", "rb"))

#file that records the meaning frequency and other information about the 
#dominance of each word
outfile = "./output/meaningfreq.txt"

#file containing the correlation between edom human and the new computational
#edom scores computed by this module.  Intended as a quick final summary of 
#the results of the comparison file.  
correlationfile = "./output/correlation.txt"

#stores the new computational measure of biggest and the original edom scores
#from humans.  Good for quick import of both datasets to R for plotting and
#additional analyses.  
bigcompfile = './output/bigcomp.txt'

#load information from original edom behaviour file.  
edomBehaviourfile = './input/eDom_biggest.txt'

###  END USER VARS ############################################################

fout = open(outfile, "w")


bigdict = {}

sofar = 0; #counter for number of items that have been processed

#tries to estimate biggest for every homonym for which dictionary vectors were
#computed in the previous module.  
for k in defsspace:
    print(str(sofar) + ": " + k) #display progress
    sofar = sofar+1;
    
    if not os.path.isfile('./critwindows/'+k+'.mat'):
        print(k +' did not have a .mat file associated with it')
    else:
        f=open('./critwindows/'+k+'.mat','r')
        def_arr = np.genfromtxt('./critwindows/'+k+'.mat')

        arr = np.zeros([len(defsspace[k]), len(def_arr)])

        for m in defsspace[k]:
            for i in range (0,len(def_arr)):
                cossim = cosine_similarity(defsspace[k][m][0], def_arr[i])
                arr[int(m)-1, i] = cossim

        #count up the number of times each critical window was most similar
        #to a particular dictionary definition.
        meaningcount = np.zeros([len(defsspace[k]), 1])

        for j in range (0, len(def_arr)):
            #initialized state; should never have a cosine this small
            #so should always be overridden.
            bigcos = -2.0;   
            winner = -1;

            for n in range(0,len(defsspace[k])):
                curVal = arr[n, j]
                if  curVal > bigcos:
                    bigcos = curVal;
                    winner = n;

            meaningcount[winner] = meaningcount[winner]+1

        #compute average statistics across all occurrences of the word
        tot = sum(meaningcount)

        #compute relative frequency for each definition.  These are stored in
        #the same format/order as the edom behavioural output to enable 
        #definition specific comparisons if desired.  
        for i in range(len(meaningcount)):
            meaningcount[i]=meaningcount[i]/tot*100;

        meaningcount = meaningcount.round();

        biggest = max(meaningcount)

        bigdict[k] = biggest;

        fout.write(k +"\t"+ str(round(biggest[0])) + "\t")

        for i in range(len(meaningcount)):
             fout.write(str(round(meaningcount[i][0]))+"\t")

        fout.write(str(tot[0]))
        fout.write("\n")

fout.close()


#compute correlation with existing eDom behavioural data.  

eDom = {}

for line in open(edomBehaviourfile):
    line = line.split()
    print(line)
    eDom[line[0]] = int(line[1])

#merge original edom with the computational edom data;
#in case of missing values, only keep the union for which we have data
#for both items.  
edomUnion = {};
for k in eDom:
    if k in bigdict:
        edomUnion[k] = eDom[k]
    else:
        print("ERROR: Missing following item in bigdict, but present in edom: "+k)

print("Number of observations in bigdict")
print(len(bigdict))

print("Number of observations in edomUnion")
print(len(bigdict))

allbiggest = np.zeros([2, len(bigdict)])
i=0;

wlist = [];

#prepare an nx2 array which has the data from behavioural and computational
#stored for each word for which we have data on both.  
for k in bigdict:
    if k in edomUnion:
        #print('running loop')
        allbiggest[0][i] = bigdict[k]
        allbiggest[1][i] = edomUnion[k]
        wlist.append([k,allbiggest[0][i],allbiggest[1][i]])
    else:
        print("ERROR: Missing following item in edomUnion: "+k)
    i=i+1


#check correlation with a couple of methods; write results to file.


print('Correlation between eDom and our method:')
print(str(np.corrcoef(allbiggest[0], allbiggest[1])[0][1].round(3)))
print('r value, p value')
print(pearsonr(allbiggest[0],allbiggest[1]))


fc = open(correlationfile, "w")
fc.write(str(np.corrcoef(allbiggest[0], allbiggest[1])[0][1])+'\r\n')
fc.write('r value, p value\r\n')
fc.write(str(pearsonr(allbiggest[0],allbiggest[1])))
fc.close()


#write all biggest to a separate file that could allow you to run correlations
#with biggest...  It would be nice to merge this with the data from the 
#meaningfreq file above, but this was not done initially so as to facilitate
#calculating information for any word, even those for which biggest data
#might not be available (e.g., polysemes)
ff = open(bigcompfile,'w');
for item in wlist:
    ff.write(item[0]+'\t'+str(int(item[1]))+'\t'+str(int(item[2]))+'\r\n')
ff.close();

    
print("\r\n")
print("task complete --- total time:")
print(datetime.now()-startTime);
print("\r\n")

