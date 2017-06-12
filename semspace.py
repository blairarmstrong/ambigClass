#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


@author: caitlin, blair

The main puropose of this module is to generae a pickled file that is suitable
#for getting the semantic vectors associated with all words that are listed
#in a frequency filtered file.
"""



from datetime import datetime
startTime = datetime.now();

import numpy as np
import nltk
import pickle

#location of SUBTL word frequency data
mostfreqfile = "./input/SUBTL_ge1.txt"
glovefile = './semspace/glove.6B.300d.txt'

#load list of words from frequency filtered list
f2 = open(mostfreqfile,"r")

mostfreq = [];
with open(mostfreqfile) as f2:
    for line in f2:
        mostfreq.append(line.strip())

sendict = {}
masterlist= []
for line in open(glovefile,'r',encoding="utf8"):
    listWords = line.split(" ")
    cleanlist = []
    for word in listWords:
        if word != "":
            cleanlist.append(word.strip())

    a = cleanlist.pop(0).lower()
    
    #filters out items so that only  alphanumeric words that
    #appear in the frequency filtered list that are not stop words are included.  
    if a.isalpha() and\
                a not in set(nltk.corpus.stopwords.words('english')) and\
                            a in mostfreq:

        cleanlist = list(map(float, cleanlist))
        cleanlist = np.array(cleanlist, dtype = float)

        sendict[a] = cleanlist

pickle.dump(sendict, open("sendict.p", "wb"))

print("\r\n")
print("task complete --- total time:")
print(datetime.now()-startTime);
print("\r\n")

from sys import getsizeof
print(getsizeof(sendict))



