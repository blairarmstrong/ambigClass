#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 15:33:36 2017

@author: caitlin
"""
import pickle
sendict2 = pickle.load(open("sendict.p", "rb"))
#print(sendict2)

a = sendict2['dog']
print(a)

b = sendict2['cats']
print(b)

