
### NOTE: This version is a forked and adapted version of the original
#code designed to run in parallel.  double check that behaviour is as expected.

from datetime import datetime
startTime = datetime.now();

#from time import sleep
import sys
import os
from os import listdir
from os.path import isfile, join
from nltk import word_tokenize, wordpunct_tokenize
import codecs
import nltk
import dill as pickle #need advanced pickling to pickle nltk lamba
import pathos.multiprocessing as multiprocessing
import numpy as np
import socket
from nltk import ConcordanceIndex
#adapted from  http://stackoverflow.com/questions/22118136/nltk-find-contexts-of-size-2k-for-a-word

#load common scripts located in single file to facilitate parallelization
sys.path.append("./")


########### USER CONFIGURABLE SETTINGS ########################################
wikidir = "./wiki/"
concorddir= './concordances/'
freqdir = "./freq/"

#location of SUBTL word frequency data
mostfreqfile = "./input/SUBTL_ge1.txt"

targFile = "./input/targets.txt"
critwindowdir = "./critwindows/"

sendictfile = 'sendict.p'

critWindowCountFile = 'critcounts.txt'

semdim = 300

if socket.gethostname() == 'neurocomp2':
    nProcs = 31;
else:
    nProcs = 3;

###############################################################################

class ConcordanceIndex2(ConcordanceIndex):
    def create_concordance(self, word, token_width=11):
        "Returns a list of contexts for @word with a context <= @token_width"
        half_width = token_width // 2
        contexts = []
        for i, token in enumerate(self._tokens):
            if token == word:
                start = i - half_width if i >= half_width else 0
                context = self._tokens[start:i + half_width + 1]
                contexts.append(context)
        return contexts


def createConcordances(fname):
    print("Processing file: "+fname)

    f = codecs.open(wikidir+fname,"r","utf-8")
    print(fname)
    raw = f.read();
    #print(fname)
    tokens = wordpunct_tokenize(raw);
    text = nltk.Text(tokens)

    lenRawText = len(text) # number of words in the cleaned dsocument.
    print("Current cleaned article length: " + str(lenRawText))

    #print(text)

    #load list of words from frequency filtered list
    f2 = open(mostfreqfile,"r")

    mostfreq = [];
    with open(mostfreqfile) as f2:
        for line in f2:
            mostfreq.append(line.strip())
    ##print("number of words in frequency file")
    #print(len(mostfreq))
    #print(mostfreq)


    #clean up the processed text as desired
    #1a.  Convert text to lowercase, remove spaces around words
    #1b.  Removing "words" that are not alphabetical.
    #2.  Remove words that are 1 character in length
    #3.  Not in the stopword list for nltk English
    #4   Only keep most frequent words as specified in external file
    words = [w.lower().strip() for w in text if w.isalpha() and
              len(w) > 1 and
              w not in set(nltk.corpus.stopwords.words('english')) and
              w in mostfreq]

    #create a new text object based on the "cleaned text"
    raw2 = " ".join(words)
    tokens2 = word_tokenize(raw2)
    text2 = nltk.Text(tokens2)

    lenCleanText = len(text2) # number of words in the cleaned dsocument.
    print("Current cleaned article length: " + str(lenCleanText))

    print("Percent of Tokens removed during cleaning")
    if lenRawText > 0:
        print((lenRawText-lenCleanText)/lenRawText*100)

    #create concordance array based on cleaned text  , pickle resulting object
    print("Calculating Concordances")
    c = ConcordanceIndex2(tokens2)
    pickle.dump(c,open(concorddir+fname, 'wb'))
    print("Completed Calculating Concordances")

    #Calculate and save frequency information for the text
    fdist = nltk.FreqDist(tokens2)
    pickle.dump(fdist,open(freqdir+fname+".freq", 'wb'))


    print("Completed processing one article")
    return lenRawText #length of words in cleaned article



def critWindows(t):
#    #####print("running target: " + t)
    sendict = pickle.load(open(sendictfile, "rb"))
    fl = [f for f in listdir(concorddir) if isfile(join(concorddir, f))]
    i = 0;

    #print('Processing critical windows for t: '+t)
    for fname in fl:
        #print("t: " + t + " f: " + fname)
        #reload in the pickeled concordance file from prev step:
        with open(concorddir+fname, 'rb') as handle:
            c = pickle.load(handle)

        l = c.create_concordance(t)
        #c.print_concordance(h)
        #print(l) #lists the concordance in memory

        #if t == 'alley':
        #    print('Alley files being created')
        f2 = open(critwindowdir+t+".txt","a")
        #if t == 'alley':
        #    print('alley.txt file created')
        f3 = open(critwindowdir+t+".mat","a")
        j=0;
        newvec = np.zeros([1, semdim]);

        for e in l:
            f2.write(' '.join(e) + "\r\n")
            j=j+1;

            for g in e:
                if g != t:
                    if g in sendict:
                        newvec = newvec+sendict[g]

            #print('\r\n')
            #print(newvec)
            #print(len(newvec[0]))
            #print(newvec.shape())
            #print('\r\n')


            newlist=newvec[0].tolist();
            #print('\r\n')

            #print(newlist)
            #print('\r\n')
            #print(len(newlist))

            newstr = ' '.join((f'{h:.6f}') for h in newlist)
            f3.write(newstr)
            f3.write('\r\n')


        f2.close();
        f3.close();
        i = i+j;



    return({t:i})


###############################################################################
#main loop to be executed by master processor
if __name__=='__main__':

    print("\r\n\r\n")

    #clear critical window directory
    torm = os.listdir(concorddir)
    for f in torm:
        #if f.endswith(".txt"):
        os.remove(join(concorddir,f))

    #clear frequency directory
    torm = os.listdir(freqdir)
    for f in torm:
        if f.endswith(".freq"):
            os.remove(join(freqdir,f))


    fl = [f for f in listdir(wikidir) if isfile(join(wikidir, f))]

    print("List of files to process")
    print(fl)
    print("\r\n")

    #initiate parallel processing to create concordance matrices
    print("Trying parallel with: "+ str(nProcs) + " processors")
    pool= multiprocessing.Pool(processes=nProcs)
    print("pool initialized")
    print("\r\n")

    #results = [pool.apply_async(createConcordances,args=(x,)) for x in fl]

    results = []
    for x in fl:
        createConcordances(x)

    #print("Waiting to display results of async processing")
    #output = [p.get() for p in results]

    #print("Total number of words after cleaning, across all files:")
    #print(sum(output))

    print("\r\n")
    print("task complete --- total time:")
    print(datetime.now()-startTime);
    print("\r\n")

    #sleep(5) #wait 5 seconds before continuing to allow residual processes
    #to clean up.
    #########################################################################
    #clear critical window directory
    torm = os.listdir(critwindowdir)
    for f in torm:
        if f.endswith(".txt"):
            os.remove(join(critwindowdir,f))
        if f.endswith(".mat"):
            os.remove(join(critwindowdir,f))

    #load list of words to get critical windows for
    targetList = open(targFile).read().splitlines();

    print("Trying parallel with: "+ str(nProcs) + " processors")
    pool= multiprocessing.Pool(processes=nProcs)
    print("pool initialized")
    print("\r\n")

    #results = [pool.apply_async(critWindows,args=(t,)) for t in targetList]
    results =[]
    for x in targetList:
        results.append(critWindows(x))
    output = results;
    print("Waiting to display results of async processing")
    #output = [p.get() for p in results]
    print("Number of critical windows for each word")
    for e in output:
        for ke in e:
            print("\t"+ke+'\t'+str(e[ke]))

    #remove empty files from the critwindow dir
    for f in os.listdir(critwindowdir):
        if os.stat(critwindowdir+f).st_size == 0:
            print(f+ " should be deleted")
            os.remove(join(critwindowdir,f))

    #remove files that have exactly one line in them.  They don't have enough
    #data to calculate a meaningful dominance score and they let you avoid
    #complications in comparison.py related to how you index a 1d vs 2d array
    #based on size to know how many rows you need to run cosines on.
    for e in output:
        for ke in e:
            if e[ke] == 1:
                print(ke + ' file only contains one row... deleting...')
                os.remove(join(critwindowdir,ke+'.txt'))
                os.remove(join(critwindowdir,ke+'.mat'))

    #write the critical counts to files:
    fcrit = open('./output/'+critWindowCountFile,'w')
    for e in output:
        for ke in e:
            fcrit.write(ke+'\t'+str(e[ke])+'\n')
    fcrit.close();

    print("\r\n")
    print("task complete --- total time:")
    print(datetime.now()-startTime);
    print("\r\n")
