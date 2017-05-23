#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 15:33:36 2017

@author: caitlin
"""
import pickle
sendict2 = pickle.load(open("sendict.p", "rb"))
#print(sendict2)

a = sendict2['translator'][0]
print(a)
b = sendict2['native'][0]
print(b)
c = sendict2['graduate'][0]
print(c)
d = sendict2['grandfather'][0]
print(d)
e = sendict2['worked'][0]
print(e)
f = sendict2['clerk'][0]
print(f)
g = sendict2['spent'][0]
print(g)
h = sendict2['childhood'][0]
print(h)
i = sendict2['described'][0]
print(i)
j = sendict2['childhood'][0]
print(j)

t = a + b + c + d + e + f + g + h + i + j

print(t)
