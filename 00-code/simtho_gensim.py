# Basic documentation:
# https://radimrehurek.com/gensim/auto_examples/core/run_core_concepts.html
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora, models, similarities
from gensim.test.utils import datapath, get_tmpfile
from gensim.similarities import Similarity
from gensim.models import word2vec
import codecs
import numpy as np
from numpy import savetxt
import re
from pprint import pprint
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib
from random import seed
from random import randint
from bs4 import BeautifulSoup
import pandas as pd
import time
import faulthandler

faulthandler.enable()

# Then we read in the entire corpus 
# - which I previously merged into a single file
# - with one document per line
# and we create an array of documents
# This is done because I want to compare documents and their text type
    
f = codecs.open('x:/data/Simtho-gensim/beth_mardutho_simtho__syriac_corpus_0.1.0_2019_11_16_Beta_Launch.vrt', 'r', 'utf-8')
print("Opened corpus file")


soup = BeautifulSoup(f, 'html.parser')
print("Parsed corpus file")


documents = []

for doc in soup.find_all('doc'):
    print(doc.get('id'))
    documents.append(doc.text)
print(len(documents))


################ CLEANUP #######################
#### NO STOP LIST
#### TWO STEPS, all within list comprehension below
#### 1. remove all tokens with a) Latin letters, b) Latin digits, c) Syriac punctuation
#### 2. remove from all tokens all bullshit characters (see uselesschars.tab)

# load chartable which are three tab-separated columns
uselesscharfile = ('x:/data/Simtho-gensim/uselesschars.tab')


# this function converts the files into a chartable dictionary
def getchartable(filename):
    chartable = {}
    with open(filename, 'r', encoding='utf-8') as f:
        charlines = f.readlines()
        for charline in charlines:
            if not re.match("^\#", charline):
                charline = charline.rstrip()
                entry = charline.split("\t")
                print(entry[2])
                key = chr(int(entry[2]))
                value = None
                chartable[key] = value
        return(chartable)

crt = getchartable(uselesscharfile)

for k in crt.keys():
    print(len(k))

# this function translates original text into the simplified transcription based on the chartable
# and deletes useless stuff
def translatechars(string, chartab):        
    newstring = string.translate(str.maketrans(chartab))      
    return(newstring)

# This creates a list of lists: a list of all tokens for every document,
# but excluding stopwords
print("Creating raw text collection...")
alltexts1 = [[word for word in document.lower().splitlines()] for document in documents]

print("Creating extraclean text collection...")
t = time.process_time()
alltexts2 = [[translatechars(word, crt) for word in document.lower().splitlines() 
              if not re.match(".*?[A-Za-z0-9܀܁܂܃܄܅܆܇܈܉܊܋܌܍]", word)] for document in documents]
print("Done, the processing took " + str(time.process_time() - t) + " seconds")

#check if shit worked
a1 = 0
for x in alltexts1:
    a1 = a1 + len(x)

a2 = 0 #8 437 331
for x in alltexts2:
    a2 = a2 + len(x)

a3 = 0
for x in alltexts2:
    a3 = a3 + len(x)

print(str(a1) + "|" + str(a2))


# calculate frequency of tokens
from collections import defaultdict
frequency = defaultdict(int)
for text in alltexts2:
    for token in text:
        frequency[token] += 1

# calculate unique tokens
dictionary = corpora.Dictionary(alltexts2)

# display the ids of unique tokens
# pprint(dictionary.token2id)


#############################################################################################################
#####################################  CREATING THE WORD2VEC MODEL ################################################
# This creates the actual word2vec model
# For info on settings, see 

print("Creating the model...")
t = time.process_time()
model = word2vec.Word2Vec(alltexts2, size=500, window=10, min_count=2, workers=4)
print("Model created, the processing took " + str(time.process_time() - t) + " seconds")
#5839 = 1.6 hours

# This calculates the collocations of the given word
print("Calculating the similarity of a word")
model.wv.most_similar('ܐܠܗܐ')

#export the model
from gensim.test.utils import get_tmpfile
from gensim.models import Word2Vec, KeyedVectors   

print("Saving the model to disk")
simthomodel = model
fname = get_tmpfile("x:\\data\\Simtho-gensim\\model\\simthovectors-size500-window10-min2.kv")
simthomodel.save(fname)
print("Model saved to the disk")

################# NEW VISUALIZATION ###################################
from sklearn.decomposition import IncrementalPCA    # inital reduction
from sklearn.manifold import TSNE                   # final reduction
import numpy as np                                  # array handling


def reduce_dimensions(model):
    num_dimensions = 2  # final num dimensions (2D, 3D, etc)

    vectors = [] # positions in vector space
    labels = [] # keep track of words to label our data again later
    for word in model.wv.vocab:
        vectors.append(model.wv[word])
        labels.append(word)

    # convert both lists into numpy vectors for reduction
    vectors = np.asarray(vectors)
    labels = np.asarray(labels)

    # reduce using t-SNE
    vectors = np.asarray(vectors)
    tsne = TSNE(n_components=num_dimensions, random_state=0)
    vectors = tsne.fit_transform(vectors)

    x_vals = [v[0] for v in vectors]
    y_vals = [v[1] for v in vectors]
    return x_vals, y_vals, labels


x_vals, y_vals, labels = reduce_dimensions(model)


import numpy
numpy.savetxt("foo.csv", labels, delimiter=",")

labels.dtype


def plot_with_plotly(x_vals, y_vals, labels, plot_in_notebook=False):
    from plotly.offline import init_notebook_mode, iplot, plot
    import plotly.graph_objs as go

    trace = go.Scatter(x=x_vals, y=y_vals, mode='text', text=labels)
    data = [trace]

    if plot_in_notebook:
        init_notebook_mode(connected=True)
        iplot(data, filename='x:\\data\\Simtho-gensim\\model\\word-embedding-plotword-embedding-plot')
    else:
        plot(data, filename='x:\\data\\Simtho-gensim\\model\\word-embedding-plot.html')




def plot_with_matplotlib(x_vals, y_vals, labels):
    import matplotlib.pyplot as plt
    import random

    random.seed(0)

    plt.figure(figsize=(12, 12))
    plt.scatter(x_vals, y_vals)

    #
    # Label randomly subsampled 25 data points
    #
    indices = list(range(len(labels)))
    selected_indices = random.sample(indices, 25)
    for i in selected_indices:
        plt.annotate(labels[i], (x_vals[i], y_vals[i]))

try:
    get_ipython()
except Exception:
    plot_function = plot_with_matplotlib
else:
    plot_function = plot_with_plotly

plot_with_plotly(x_vals, y_vals, labels)


simres = model.wv.most_similar('ܐܠܗܐ')

coordinates = np.column_stack((x_vals, y_vals))

np.stack((coordinates, labels))

coordinates.shape
labels.shape
