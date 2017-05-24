#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 13:47:13 2017

@author: caitlin
"""
     
#import nltk
import pickle
import numpy as np
import scipy
from scipy import spatial
import math

def square_rooted(x):

    return (math.sqrt(sum([a*a for a in x])))

def cosine_similarity(x,y):

    numerator = sum(a*b for a,b in zip(x,y))
    denominator = square_rooted(x)*square_rooted(y)
    return (numerator/float(denominator))
    


                        
#Import dictionary vectors from pickled file (defsspace)
defsspace = pickle.load(open("./eDom_filter/defsspace/defsspace.p", "rb"))
outfile = "./output/meaningfreq.txt"
correlationfile = "./output/correlation.txt"
    
#Import wikipedia .mat files, convert txt to matrix arrays 
 
fout = open(outfile, "w")

ds = {}
ds['bank'] = defsspace['bank']
ds['ear'] = defsspace['ear']
ds['compound'] = defsspace['compound']
defsspace = ds;

bigdict = {}

for k in defsspace:
    
    f=open('./critwindows/'+k+'.mat','r')
    def_arr = np.genfromtxt('./critwindows/'+k+'.mat')

    arr = np.zeros([len(defsspace[k]), len(def_arr)])

    for m in defsspace[k]:
        print(defsspace[k][m][0])
        for i in range (0,len(def_arr)):
            #print(i)
            cossim = cosine_similarity(defsspace[k][m][0], def_arr[i])
            arr[int(m)-1, i] = cossim
                
    #find out which meaning won on each row.
    meaningcount = np.zeros([len(defsspace[k]), 1])
    
    
    for j in range (0, len(def_arr)):
        #find over m rows which is largest
        bigcos = -2.0
        winner = -1;
        #n=-1
        for n in range(0,len(defsspace[k])):
            curVal = arr[n, j]
            if  curVal > bigcos:
                bigcos = curVal;
                winner = n;

        meaningcount[winner] = meaningcount[winner]+1
        
    tot = sum(meaningcount)
    
    for i in range(len(meaningcount)):
        meaningcount[i]=meaningcount[i]/tot*100;
    
    meaningcount = meaningcount.round();
                                     
    print(meaningcount)
    
    biggest = max(meaningcount)
    
    bigdict[k] = biggest;
    
    fout.write(k +"\t"+ str(round(biggest[0])) + "\t") 
    
    for i in range(len(meaningcount)):
         fout.write(str(round(meaningcount[i][0]))+"\t")
        
    fout.write(str(tot[0]))
    fout.write("\n")
    
    
    
    
fout.close()

    
#compute correlation for all words that we have found so far

#load in eDom biggest file
#read into dictionary line by line, only two columns, so use string.split to break into eleents
# where first item

eDom = {}

for line in open('./input/eDom_biggest.txt'):
    line = line.split()
    eDom[line[0]] = int(line[1])
    
edomUnion = {};

for k in bigdict:
    edomUnion[k] = eDom[k]
    
allbiggest = np.zeros([2, len(edomUnion)])
i=0;
for k in bigdict:
    allbiggest[0][i] = bigdict[k]
    allbiggest[1][i] = edomUnion[k]
    i=i+1

#https://stackoverflow.com/questions/26714048/numpy-arrays-correlation
def corr_pearson(x, y):

    """
    Compute Pearson correlation.
    """

    x_mean = np.mean(x, axis=0)
    x_stddev = np.std(x, axis=0)

    y_mean = np.mean(y, axis=0)
    y_stddev = np.std(y, axis=0)

    x1 = (x - x_mean)/x_stddev
    y1 = (y - y_mean)/y_stddev

    x1y1mult = x1 * y1

    x1y1sum = np.sum(x1y1mult, axis=0)

    corr = x1y1sum/20.

    return corr

    
print(corr_pearson(allbiggest[0], allbiggest[1]))
print('Correlation between eDom and our method:')
print(np.corrcoef(allbiggest[0], allbiggest[1])[0][1].round(decimals=3))

fc = open(correlationfile, "w")
fc.write(str(np.corrcoef(allbiggest[0], allbiggest[1])[0][1].round(decimals=3)))
fc.close()




    
    



