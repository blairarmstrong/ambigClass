 
#cleans the processedWords folder so that it only contains the target words
#listed in the fname file.  This greatly speeds searching of this directory
#in all future searches.

import glob
from shutil import copyfile
import os
import re
from nltk import wordpunct_tokenize
import nltk
import copy
import pickle
#import dill as pickle #need advanced pickling to pickle nltk lamba 
import numpy as np

########### USER CONFIGURABLE SETTINGS ########################################

#location of SUBTL word frequency data
mostfreqfile = "./input/SUBTL_ge1.txt"

sendictfile = '../sendict.p'

defsspacedir='./defsspace/'
defsspace_fn='defsspace.p'

###############################################################################

fname = "./input/586AmbiguousWords_-mole-con-rack.txt"
defdir = './processedWords/'
outdir = './targetwords/'


with open(fname) as f:
    targets = f.readlines()
targets = [x.strip() for x in targets]

for t in targets:
    print("Processing: " + t )
    for e in  glob.glob(defdir+t+'[.]singleword.[0-9].*'):
        copyfile(e,outdir+os.path.basename(e))

#run in separate loop to allow all files to have been moved over above, this
#avoids trying to access a just-created file in case of bottlenecks.
defs = {};

for t in targets:
    for e in  glob.glob(outdir+t+'[.]singleword.[0-9].*'):
        #regex on filename to determine which meaning it corrsponds to

        m = re.search(t+'\.singleword\.([0-9])*',os.path.basename(e).lower())
        n = m.group(1)

        f = open(outdir+os.path.basename(e))
        s = f.read();

        #add string definition to the key for that word.

        if t in defs:
            #definition already exists
            pass
        else:
            #create new definition dictionary
            defs[t] = {}

        #if specific definition already exists, append to that definition
        if len(defs[t]) > 0  and n in defs[t]:
            #definition number already exists, can just append to that definition
            defs[t][n] = defs[t][n] + ' ' + s;
        else:
            defs[t][n] = s;

        f.close()


mostfreq = [];
with open(mostfreqfile) as f2:
    for line in f2:
        mostfreq.append(line.strip()) 
        
#clean up the definition array.
#j is index of meanings, k is index of number that corresponds to meaning
for k in defs:
    for j in defs[k]:
        #clean up the file
#        print(defs[k][j])

        #replace the following with the code needed to clean up the definition
        #in a similar way to the original clean up of the file.  Then, replace
        #defs[k][j] with the cleaned output.  So, something like:
                   
        #load list of words to get critical windows for
        #targetList = open(targFile).read().splitlines();

        
        s = defs[k][j]
        
        tokens = wordpunct_tokenize(s);
        text = nltk.Text(tokens)
        
        #clean up s
        words = [w.lower().strip() for w in text if w.isalpha() and 
                 len(w) > 1 and 
          w not in set(nltk.corpus.stopwords.words('english')) and
          w in mostfreq and
          w != k]
        
        raw = " ".join(words)
        #
        #
        defs[k][j] = raw;

defsspace = copy.deepcopy(defs)
  
#location of sendict
sendict = pickle.load(open(sendictfile, "rb")) 

for k in defsspace:
    for j in defsspace[k]:
        #clean up the file
        print(defsspace[k][j])
        
        s = defsspace[k][j]
        
        tokens = wordpunct_tokenize(s);
                                   
        #open 1, 400 array
        arr = np.zeros([1, 400]);
        #load semspace vector
        
        
        #define an zero vector
        for t in tokens:
            #arr + semspace vector for t;
            arr = arr + sendict[t]
        defsspace[k][j] = arr;
            
            
#pickle defs and sendict
#pickle.dump(c,open(defs+sendict, 'wb'))  
pickle.dump(defsspace,open(defsspacedir+defsspace_fn, 'wb'))  