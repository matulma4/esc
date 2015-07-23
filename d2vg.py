
from os import path
from w2vg import load_data
from gensim import models
import logging

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    fname = "newmodel.doc2vec"
    if path.isfile(fname):
        model = models.Doc2Vec.load(fname)
    else:
        dataset = load_data('text8')
        model = models.Doc2Vec(dataset, size=100, window=5, min_count=5, workers=4)
        model.save(fname)

    print model.most_similar("SENT_0")
    print model.most_similar("SENT_132")
    print model.most_similar("SENT_8923")
    print model.most_similar("SENT_12441")