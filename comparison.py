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
    
#Import wikipedia .mat files, convert txt to matrix arrays  

ds = {}
ds['bank'] = defsspace['bank']

defsspace = ds;

for k in defsspace:
    
    f=open('./critwindows/'+k+'.mat','r')
    def_arr = np.genfromtxt('./critwindows/'+k+'.mat')

    for m in defsspace[k]:
        print(defsspace[k][m][0])
        for i in range (0,len(def_arr)):
            #print(i)
            cossim = cosine_similarity(defsspace[k][m][0], def_arr[i])
            print(cossim)
        
        #Need to calculate and save similarity of each word for each entry with cos 
        #cos (gives value between -1 and 1, see what meaning is closest to 1). 
        #Two vectors with cosine of 1 have same orientation, 90degrees have similarity of 0, 
            #opposed have similarity of -1
        # to round cosine, use format(round(cosine, 3)) where 3 is number of decimals
        #Come up with scoring regime
        
       

    #for k in defsspace
        #where k is string label ('bank')
        #open k.mat in other folder that we point it to that stores .mat file for k (bank.mat)
        #For every line in bank.mat convert into array
        #Compare array to all of the meaning vectors in k
        
 #Import wikipedia files from .mat files, will need to convert from txt to matricies
    #either one line at a time or go in and subscript it (maybe for line in file: cpnvert string into np array
    #go string to list to np array
    
#add in comparison (winner takes all?)


