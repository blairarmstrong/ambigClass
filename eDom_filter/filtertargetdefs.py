
#cleans the processedWords folder so that it only contains the target words
#listed in the fname file.  This greatly speeds searching of this directory
#in all future searches.

import glob
from shutil import copyfile
import os
import re

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


#clean up the definition array.
for k in defs:
    for j in defs[k]:
        #clean up the file
        print(defs[k][j])

        #replace the following with the code needed to clean up the definition
        #in a similar way to the original clean up of the file.  Then, replace
        #defs[k][j] with the cleaned output.  So, something like:

        s = defs[k][j]
        #clean up s
        #
        #
        #
        defs[k][j] = s;




