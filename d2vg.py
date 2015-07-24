import sys
from os import path
from w2vg import load_data
from gensim import models,utils
from gensim.models.doc2vec import TaggedDocument
import logging
from collections import namedtuple
import numpy as np
class LabeledLineSentence(object):
    def __init__(self, filename):
        self.filename = filename
        self.data = load_data(filename)
    def __iter__(self):
        for uid, line in enumerate(self.data):
            yield TaggedDocument(words=line.split(), labels=['SENT_%s' % uid])

if __name__ == "__main__":

    SentimentDocument = namedtuple('SentimentDocument', 'words tags split sentiment')

    alldocs = []  # will hold all docs in original order
    with open('aclImdb/alldata-id.txt') as alldata:
        for line_no, line in enumerate(alldata):
            tokens = utils.to_unicode(line).split()
            words = tokens[1:]
            tags = [line_no] # `tags = [tokens[0]]` would also work at extra memory cost
            split = ['train','test','extra','extra'][line_no//25000]  # 25k train, 25k test, 25k extra
            sentiment = [1.0, 0.0, 1.0, 0.0, None, None, None, None][line_no//12500] # [12.5K pos, 12.5K neg]*2 then unknown
            alldocs.append(SentimentDocument(words, tags, split, sentiment))

    train_docs = [doc for doc in alldocs if doc.split == 'train']
    test_docs = [doc for doc in alldocs if doc.split == 'test']
    doc_list = alldocs[:]  # for reshuffling per pass

    print('%d docs: %d train-sentiment, %d test-sentiment' % (len(doc_list), len(train_docs), len(test_docs)))

    name = sys.argv[1]
    dist_mem = int(sys.argv[2])
    hier_soft = int(sys.argv[3])
    neg = int(sys.argv[4])
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    fname = str(name)+".doc2vec"
    if path.isfile(fname):
        model = models.Doc2Vec.load(fname)
    else:
        model = models.Doc2Vec(size=100, window=5, min_count=5, workers=4,negative=neg,hs=hier_soft,dm=dist_mem)
        model.save(fname)

    doc_id = np.random.randint(model.docvecs.count)  # pick random doc, re-run cell for more examples
    # model = np.random.choice(model)  # and a random model
    sims = model.docvecs.most_similar(doc_id, topn=model.docvecs.count)  # get *all* similar documents
    f = open(name+'.out','w')
    f.write(u'TARGET (%d): <%s>\n' % (doc_id, ' '.join(alldocs[doc_id].words)))
    f.write(u'SIMILAR/DISSIMILAR DOCS PER MODEL %s:\n' % model)
    for label, index in [('MOST', 0), ('MEDIAN', len(sims)//2), ('LEAST', len(sims) - 1)]:
        f.write(u'%s %s: <%s>\n' % (label, sims[index], ' '.join(alldocs[sims[index][0]].words)))