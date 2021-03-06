# Basic documentation:
# https://radimrehurek.com/gensim/auto_examples/core/run_core_concepts.html
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora, models, similarities
from gensim.test.utils import datapath, get_tmpfile
from gensim.similarities import Similarity
from gensim.models import word2vec
from bs4 import BeautifulSoup
import codecs
import pandas as pd
import time
import pickle
import re
import glob
import faulthandler


faulthandler.enable()

# Then we read in the entire corpus 
# - which I previously merged into a single file
# - with one document per line
# and we create an array of documents
# This is done because I want to compare documents and their text type

# sentences = []

# for x in glob.glob('x:/data/Malti-gensim/vrt/*.vrt'):    

#     f = codecs.open(x, 'r', 'utf-8')
#     print("Opened corpus file " + str(x))
    
    
#     soup = BeautifulSoup(f, 'html.parser')
#     print("Parsed corpus file  " + str(x))
    
#     # for doc in soup.find_all('doc'):    
#     #     documents.append(doc.text)
#     # print(len(documents))

#     for s in soup.find_all('s'):    
#         sentences.append(s.text)

# print(len(sentences))


# with open('x:/data/Malti-gensim/maltiv3-sentences.pkl', 'wb') as pickle_file:
#     pickle.dump(sentences, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)

##### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ############################################
#########################################################################################################
###### START HERE WHEN PICKLED ##########################################################################

print("Opening the pickled file")
with open('x:/data/Malti-gensim/maltiv3-sentences.pkl', 'rb') as pickle_load:
    sentences = pickle.load(pickle_load)

alltexts1 = [[word for word in sentence.lower().splitlines() 
              if not re.match(".*[0-9].*|.*-", word)] for sentence in sentences]
print("Text collection created")


#check if shit worked
#a1 = 0
#for x in alltexts:
#    a1 = a1 + len(x)

# a2 = 0 #8 437 331
# for x in alltexts1:
#     a2 = a2 + len(x)

# print(str(a2))


# # calculate frequency of tokens
# from collections import defaultdict
# frequency = defaultdict(int)
# for text in alltexts1:
#     for token in text:
#         frequency[token] += 1
# print("Frequencies counted")

# calculate unique tokens
#dictionary = corpora.Dictionary(alltexts1)

##########################################################################################################
#####################################  CREATING THE WORD2VEC MODEL #######################################
# This creates the actual word2vec model
# For info on settings, see 


print("Creating the model...")
t = time.process_time()
model = word2vec.Word2Vec(alltexts1, size=300, window=10, min_count=10, workers=4)
print("Model created, the processing took " + str(time.process_time() - t) + " seconds")
#5839 = 1.6 hours

# This calculates the collocations of the given word
print("Calculating the similarity of a word")
model.wv.most_similar("tajjeb")

finalmodel = model
fname = get_tmpfile("x:\\data\\Malti-gensim\\model\\maltiv3-s-size300-window10-min10.kv")
finalmodel.save(fname)