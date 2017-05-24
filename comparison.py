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
    
#Import wikipedia .mat files, convert txt to matrix arrays 
 
fout = open(outfile, "w")

ds = {}
ds['bank'] = defsspace['bank']
ds['compound'] = defsspace['compound']
defsspace = ds;

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
    
    fout.write(k +"\t"+ str(round(biggest[0])) + "\t") 
    
    for i in range(len(meaningcount)):
         fout.write(str(round(meaningcount[i][0]))+"\t")
        
    fout.write(str(tot[0]))
    fout.write("\n")
    
    
    
    
fout.close()
    
    
    

    
    



