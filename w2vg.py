# -*- coding: utf-8 -*-
# Word2Vec gensim
import os.path

from gensim import models
import numpy as np
# from nltk.corpus import gutenberg
import logging
class MySentences(object):
    def __init__(self,fname):
        self.fname = fname
    def __iter__(self):
        for line in open(self.fname):
            yield line.split()
def load_data(fname):
    np.random.seed(11)
    words = [line for line in open(fname)]
    words = words[0].split()
    length = len(words)
    count = 0
    dataset = []
    while count < length:
        sent_len = 20# int(np.random.random() * 5) + 7
        sent_end = count + sent_len
        if sent_end > length:
            sent_end = length
        dataset.append(words[count:sent_end])
        count = sent_end
    return dataset

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    fname = "model2.word2vec"
    if os.path.isfile(fname):
        model = models.Word2Vec.load(fname)
    else:
        dataset = MySentences('temp.raw_text')# [line.split() for line in open('temp.raw_text')]
        model = models.Word2Vec(dataset, size=16, window=5, min_count=10, workers=4)
        model.save(fname)
    # print(model.syn0)
    for doc in model.most_similar(positive=['krab', 'ruka'], negative=['člověk']):
        print unicode(doc[0],'utf-8'),str(doc[1])
    print('--------------------------------------')
    for doc in model.most_similar(positive=['nafta', 'člověk'], negative=['jídlo']):
        print unicode(doc[0],'utf-8'),str(doc[1])
    print('--------------------------------------')
    for doc in model.most_similar(positive=['silnice', 'vlak'], negative=['kolej']):
        print unicode(doc[0],'utf-8'),str(doc[1])
    print('--------------------------------------')
    #for doc in model.most_similar(positive=['žena', 'král'], negative=['muž'])
    #    print unicode(doc,'utf-8')
    # print unicode(,'utf-8')
    # print model.most_similar(positive=['Paris', 'Spain'], negative=['Madrid'])
    # print model.doesnt_match("Paris Berlin Japan Tokyo".split())
    print unicode(model.doesnt_match("bratr sestra auto strýc".split()),'utf-8')