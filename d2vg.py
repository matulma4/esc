import sys
from os import path
from w2vg import load_data
from gensim import models
from gensim.models.doc2vec import TaggedDocument
import logging
class LabeledLineSentence(object):
    def __init__(self, filename):
        self.filename = filename
        self.data = load_data(filename)
    def __iter__(self):
        for uid, line in enumerate(self.data):
            yield TaggedDocument(words=line.split(), labels=['SENT_%s' % uid])
if __name__ == "__main__":
    name = sys.argv[1]
    dist_mem = sys.argv[2]
    hier_soft = sys.argv[3]
    neg = sys.argv[4]
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    fname = str(name)+".doc2vec"
    if path.isfile(fname):
        model = models.Doc2Vec.load(fname)
    else:
        dataset = LabeledLineSentence
        model = models.Doc2Vec(dataset, size=100, window=5, min_count=5, workers=4,negative=neg,hs=hier_soft,dm=dist_mem)
        model.save(fname)

    print model.most_similar("SENT_0")
    print model.most_similar("SENT_132")
    print model.most_similar("SENT_8923")
    print model.most_similar("SENT_12441")