


from datetime import datetime
startTime = datetime.now();

from sys import getsizeof


#from https://stackoverflow.com/questions/37793118/load-pretrained-glove-vectors-in-python
def loadGloveModel(gloveFile):
    print("Loading Glove Model")
    f = open(gloveFile,'r',encoding="utf8")
    model = {}
    for line in f:
        splitLine = line.split()
        word = splitLine[0]
        print(word)
        embedding = [float(val) for val in splitLine[1:]]
        model[word] = embedding
    print("Done.",len(model)," words loaded!")
    f.close()
    return model


senddict = loadGloveModel('./semspace/glove.6B.50d.txt')

print("size of glove model")
print(getsizeof(senddict))

#pickle.dump(sendict, open("sendict_glove.p", "wb"))


print("\r\n")
print("task complete --- total time:")
print(datetime.now()-startTime);
print("\r\n")
