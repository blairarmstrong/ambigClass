#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 13:47:13 2017

@author: caitlin
"""

#import nltk

from datetime import datetime
startTime = datetime.now();


import scipy;
import pickle
import numpy as np
#import scipy
#from scipy import spatial
import math
import os.path

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

bigcompfile = './output/bigcomp.txt'


#Import wikipedia .mat files, convert txt to matrix arrays

fout = open(outfile, "w")

#ds = {}
#ds['chow'] = defsspace['chow']
#ds['ear'] = defsspace['ear']
#ds['compound'] = defsspace['compound']
#defsspace = ds;

bigdict = {}

sofar = 0;
for k in defsspace:
    print(k);
    print(sofar)
    sofar = sofar+1;
    if not os.path.isfile('./critwindows/'+k+'.mat'):
        print(k +' did not have a .mat file associated with it')
    else:
        f=open('./critwindows/'+k+'.mat','r')
        def_arr = np.genfromtxt('./critwindows/'+k+'.mat')

        arr = np.zeros([len(defsspace[k]), len(def_arr)])

        for m in defsspace[k]:
            for i in range (0,len(def_arr)):
#                print("full critwindow file"+str(def_arr))
#                print("Details of defspace")
#                print(k)
#                print(defsspace[k][m][0])
#                print("Defails of def arr")
#                print(def_arr[i])
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

        #print(meaningcount)

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
    print(line)
    eDom[line[0]] = int(line[1])

edomUnion = {};

print("Printing bigdict")
print(bigdict)

for k in eDom:
    if k in bigdict:
        edomUnion[k] = eDom[k]
    else:
        print("ERROR: Missing following item in bigdict, but present in edom: "+k)

print("Number of observations in bigdict")
print(len(bigdict))

print("Number of observations in edomUnion")
print(len(bigdict))
###---> below used to be edomUnion instead of bigdict.
allbiggest = np.zeros([2, len(bigdict)])
i=0;

wlist = [];


for k in bigdict:
    if k in edomUnion:
        #print('running loop')
        allbiggest[0][i] = bigdict[k]
        allbiggest[1][i] = edomUnion[k]
        wlist.append([k,allbiggest[0][i],allbiggest[1][i]])
    else:
        print("ERROR: Missing following item in edomUnion: "+k)
    i=i+1

##https://stackoverflow.com/questions/26714048/numpy-arrays-correlation
#def corr_pearson(x, y):
#    #### SOMETHING SEEMS WRONG WITH THIS METHOD...  USE NUMPY
#    """
#    Compute Pearson correlation.
#    """
#
#    x_mean = np.mean(x, axis=0)
#    x_stddev = np.std(x, axis=0)
#
#    y_mean = np.mean(y, axis=0)
#    y_stddev = np.std(y, axis=0)
#
#    x1 = (x - x_mean)/x_stddev
#    y1 = (y - y_mean)/y_stddev
#
#    x1y1mult = x1 * y1
#
#    x1y1sum = np.sum(x1y1mult, axis=0)
#
#    corr = x1y1sum/20.
#
#    return corr


from scipy.stats.stats import pearsonr

#print(corr_pearson(allbiggest[0], allbiggest[1]))
print('Correlation between eDom and our method:')
print(str(np.corrcoef(allbiggest[0], allbiggest[1])[0][1].round(3)))
print('r value, p value')
print(pearsonr(allbiggest[0],allbiggest[1]))
#print(np.corrcoef(allbiggest[0], allbiggest[1])[0][1].round(decimals=3))




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



