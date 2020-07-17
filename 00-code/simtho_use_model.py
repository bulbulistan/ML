import time
import pandas as pd
import numpy as np
from sklearn.manifold import TSNE
from gensim.test.utils import get_tmpfile
from gensim.models import KeyedVectors

fname2 = get_tmpfile("x:\\data\\Simtho-gensim\\model\\simthovectors-size300-window10-min25.kv")
word_vectors = KeyedVectors.load(fname2, mmap='r')


try:
    result = word_vectors.wv.most_similar("ܝܘܡܐ")
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
X = word_vectors[vocab]


tsne = TSNE(n_components=2, random_state=0)

t = time.process_time()
X_tsne = tsne.fit_transform(X)
print("Model created, the processing took " + str(time.process_time() - t) + " seconds")


df = pd.DataFrame(X_tsne, index=vocab, columns=['x', 'y'])

df.to_csv(r'x:\\data\\Simtho-gensim\\model\\simtho999-10-2.csv')