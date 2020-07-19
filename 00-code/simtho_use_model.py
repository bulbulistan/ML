import time
import pandas as pd
import numpy as np
from sklearn.manifold import TSNE
from gensim.test.utils import get_tmpfile
from gensim.models import KeyedVectors
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

fname2 = get_tmpfile("x:\\data\\Simtho-gensim\\model\\simthovectors-size300-window10-min25.kv")
word_vectors = KeyedVectors.load(fname2, mmap='r')


try:
    result = word_vectors.wv.most_similar("ܡܠܟܬܐ", topn=20)    
except:
    print("This word is not in the corpus")

print(result)


result = word_vectors.most_similar(positive=['ܐܢܬܬܐ', 'ܡܠܟܐ'], negative=['ܓܒܪܐ'])
print("{}: {:.4f}".format(*result[0]))

word_vectors.wv.vocab["ܠܘܬ"].count

############# Also this:
### https://stackoverflow.com/questions/43776572/visualise-word2vec-generated-from-gensim
### transform to TSNE
vocab = list(word_vectors.wv.vocab)

t = time.process_time()
X = word_vectors[vocab]
print("Vectors retrieved, the processing took " + str(time.process_time() - t) + " seconds")
#million took 3 seconds - this is not a problem

tsne = TSNE(n_components=2, random_state=0, verbose=10)
print(tsne)
print("Beginning the TSNE transformation...")
t = time.process_time()
X_tsne = tsne.fit_transform(X)
print("TSNE conversion completed, the processing took " + str(time.process_time() - t) + " seconds")


df = pd.DataFrame(X_tsne, index=vocab, columns=['x', 'y'])

df.to_csv(r'x:\\data\\Simtho-gensim\\model\\simtho300-10-2.csv')