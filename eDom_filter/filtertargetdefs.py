
#cleans the processedWords folder so that it only contains the target words
#listed in the fname file.  This greatly speeds searching of this directory
#in all future searches.

import glob
from shutil import copyfile
import os

fname = "./input/586AmbiguousWords_-mole-con-rack.txt"
defdir = './processedWords/'
outdir = './targetwords/'


with open(fname) as f:
    targets = f.readlines()
targets = [x.strip() for x in targets]

for t in targets:
    print("Processing: " + t )
    for e in  glob.glob(defdir+t+'[.]singleword.[0-9].*'):
        print("copying")
        copyfile(e,outdir+os.path.basename(e))

