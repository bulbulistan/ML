# Basic documentation:
# https://radimrehurek.com/gensim/auto_examples/core/run_core_concepts.html
import logging
from gensim import corpora, models, similarities
from gensim.test.utils import datapath, get_tmpfile
from gensim.similarities import Similarity
from gensim.models import word2vec
import codecs
import numpy as np
from pprint import pprint
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import pickle
import re

# Then we read in the entire corpus 
# - which I previously merged into a single file
# - with one document per line
# and we create an array of documents
# This is done because I want to compare documents and their text type

f = codecs.open('x:/data/Malti-gensim/maltiv3.vrt', 'r', 'utf-8')
print("Opened corpus file")


soup = BeautifulSoup(f, 'html.parser')
print("Parsed corpus file")

documents = []

for doc in soup.find_all('doc'):
    #print(doc.get('id'))
    documents.append(doc.text)
print(len(documents))


with open('x:/data/Malti-gensim/maltiv3.pkl', 'wb') as pickle_file:
    pickle.dump(documents, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)

##### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ############################################
#########################################################################################################
###### START HERE WHEN PICKLED ##########################################################################

print("Opening the pickled file")
with open('x:/data/Malti-gensim/maltiv3.pkl', 'rb') as pickle_load:
    documents = pickle.load(pickle_load)

alltexts1 = [[word for word in document.lower().splitlines() 
              if not re.match("[0-9]+|.*?\-", word)] for document in documents]
print("Text collection created")

# calculate frequency of tokens
from collections import defaultdict
frequency = defaultdict(int)
for text in alltexts1:
    for token in text:
        frequency[token] += 1
print("Frequencies counted")

# calculate unique tokens
#dictionary = corpora.Dictionary(alltexts1)

##########################################################################################################
#####################################  CREATING THE WORD2VEC MODEL #######################################
# This creates the actual word2vec model
# For info on settings, see 

print("Creating the model...")
t = time.process_time()
model = word2vec.Word2Vec(alltexts1, size=300, window=10, min_count=5, workers=4)
print("Model created, the processing took " + str(time.process_time() - t) + " seconds")
#5839 = 1.6 hours

# This calculates the collocations of the given word
print("Calculating the similarity of a word")
model.wv.most_similar("tajjeb")

simthomodel = model
fname = get_tmpfile("x:\\data\\Malti-gensim\\model\\maltiv3-size300-window10-min5.kv")
simthomodel.save(fname)