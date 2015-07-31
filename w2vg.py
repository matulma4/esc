# -*- coding: utf-8 -*-
# Word2Vec gensim
import os.path
import sys
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
    data_name = sys.argv[1]
    model_name = sys.argv[2]
    fname = model_name + ".word2vec"
    if os.path.isfile(fname):
        model = models.Word2Vec.load(fname)
    else:
        dataset = MySentences(data_name + '.raw_text') # [line.split() for line in open('temp.raw_text')]
        model = models.Word2Vec(dataset, sg=int(sys.argv[3]),size=int(sys.argv[4]),window=int(sys.argv[5]),alpha=int(sys.argv[6])/1000,seed=37,
                                min_count=int(sys.argv[7]),sample=0.00005,workers=4,hs=int(sys.argv[8]),negative=int(sys.argv[9]),iter=int(sys.argv[10]))
        model.save(fname)
    # print(model.syn0)
    f = open(fname+'.out','w')
    for doc in model.most_similar(positive=['krab', 'ruka'], negative=['člověk']):
        f.write(doc[0].encode('utf-8')+" "+str(doc[1]))
    print('--------------------------------------')
    for doc in model.most_similar(positive=['nafta', 'člověk'], negative=['jídlo']):
        f.write(doc[0].encode('utf-8')+" "+str(doc[1]))
    f.write('--------------------------------------')
    for doc in model.most_similar(positive=['silnice', 'vlak'], negative=['kolej']):
        f.write(doc[0].encode('utf-8')+" "+str(doc[1]))
    f.write('--------------------------------------')
    #for doc in model.most_similar(positive=['žena', 'král'], negative=['muž'])
    #    print unicode(doc,'utf-8')
    # print unicode(,'utf-8')
    # print model.most_similar(positive=['Paris', 'Spain'], negative=['Madrid'])
    # print model.doesnt_match("Paris Berlin Japan Tokyo".split())
    f.write(model.doesnt_match("bratr sestra auto strýc".split()).encode('utf-8'))
    f.close()
    # model.accuracy('questions-words.txt')