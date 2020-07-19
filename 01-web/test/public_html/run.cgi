#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import cgi
import json
import csv
import cgitb; cgitb.enable(display=1, logdir="/home/bulbul/cgistuff")
from gensim.test.utils import get_tmpfile
from gensim.models import KeyedVectors

#first get the input data
data = cgi.FieldStorage()
word = data.getvalue('input_word')

#get csv data
allWords = {}
with open("/var/www/html/syrmodel/simtho999-10-25.csv", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=",")
    next(reader)
    for x in reader:        
        allWords[x[0]] = [float(x[1]), float(x[2])]        

#in case the user inputs nothing
if word == None:
    print("Content-Type: text/html\n")
    print("Please enter a word")

else:    
    #import the model
    fname2 = get_tmpfile("/var/www/html/syrmodel/simthovectors-size999-window10-min25.kv")
    word_vectors = KeyedVectors.load(fname2, mmap='r')

    print("Content-Type: text/html\n")

    try:
        modelOutput = word_vectors.wv.most_similar(word, topn=10)
        queryResults = dict(modelOutput)
        
        for key in queryResults:
            x = allWords[key]
            x.append(queryResults[key])
            queryResults[key] = x

        print(json.dumps(queryResults))
    except:
        print("The word " + word + " is not in the corpus")