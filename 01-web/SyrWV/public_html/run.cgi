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

#variables
model = data.gevalue('');


#get csv data
allWords = {}

# this is a list of tokens with x and y coordinates created by means of a t-sne transformation
# from the model below
# they are added to a dictionary with tokens (as they are unique) as keys and a two-item list
# containing the coordinates
#with open("/var/www/html/maltimodel/maltiv3-s-300-10-10.csv", encoding="utf-8") as f:
with open("/var/www/html/syrmodel/simtho300-10-2.csv", encoding="utf-8") as f:
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
    fname2 = get_tmpfile("/var/www/html/syrmodel/simthovectors-size300-window10-min2.kv")
    #fname2 = get_tmpfile("/var/www/html/maltimodel/maltiv3-s-size300-window10-min10.kv")
    word_vectors = KeyedVectors.load(fname2, mmap='r')

    print("Content-Type: text/html\n")

    try:
        modelOutput = word_vectors.wv.most_similar(word, topn=10)
        queryResults = dict(modelOutput) # this converts the output to a dictionary with tokens as keys and similarity indexes as values        
        queryResults[word] = 1 # adds the queried word with the value 1, duh
        
        # compare the two dictionaries
        # adds the coordinates to the dictionary 
        for key in queryResults:
            x = allWords[key]
            x.append(queryResults[key])
            queryResults[key] = x

        print(json.dumps(queryResults))
    except:
        print("The word " + word + " is not in the corpus")