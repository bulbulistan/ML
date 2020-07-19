import time
import pandas as pd
import numpy as np
from gensim.test.utils import get_tmpfile
from gensim.models import KeyedVectors
from MulticoreTSNE import MulticoreTSNE as TSNE
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

fname2 = get_tmpfile("/mnt/x/data/Malti-gensim/model/maltiv3-s-size300-window10-min10.kv")

print("Loading vectors from " + fname2)
word_vectors = KeyedVectors.load(fname2, mmap='r')

vocab = list(word_vectors.wv.vocab)

t = time.process_time()
X = word_vectors[vocab]
print("Vectors retrieved, the processing took " + str(time.process_time() - t) + " seconds")

tsne = TSNE(n_jobs=4, verbose=1)
print(tsne)
print("Beginning the TSNE transformation...")
t = time.process_time()
X_tsne = tsne.fit_transform(X)
print("TSNE conversion completed, the processing took " + str(time.process_time() - t) + " seconds")


df = pd.DataFrame(X_tsne, index=vocab, columns=['x', 'y'])
df.to_csv(r'/mnt/x/data/Malti-gensim/model/maltiv3-s-300-10-10.csv')