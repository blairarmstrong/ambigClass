#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 08:21:08 2017

@author: caitlin, blair
Illustration of cosine similarity.  Useful to test if the reference vectors
are good  for basic similarity comparisons.

"""

import pickle
import math

def square_rooted(x):

    return (math.sqrt(sum([a*a for a in x])))

def cosine_similarity(x,y):

    numerator = sum(a*b for a,b in zip(x,y))
    denominator = square_rooted(x)*square_rooted(y)
    return (numerator/float(denominator))

sendict = pickle.load(open('./sendict.p', "rb"))

print(cosine_similarity(sendict['doctor'], sendict['nurse']))
print(cosine_similarity(sendict['doctor'], sendict['mountain']))
print(cosine_similarity(sendict['mountain'], sendict['valley']))
print(cosine_similarity(sendict['doctor'], sendict['needle']))
print(cosine_similarity(sendict['radio'], sendict['stereo']))
print(cosine_similarity(sendict['curtains'], sendict['drapes']))
