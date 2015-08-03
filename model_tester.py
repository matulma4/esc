# -*- coding: utf-8 -*-
from gensim import models
import sys

if __name__ == "__main__":
    model = models.Word2Vec.load(sys.argv[1])
    f = open(sys.argv[1]+'.out','w')
    for doc in model.most_similar(positive=['krab', 'ruka'], negative=['člověk']):
        f.write(doc[0]+" "+str(doc[1]))
    print('--------------------------------------')
    for doc in model.most_similar(positive=['nafta', 'člověk'], negative=['jídlo']):
        f.write(doc[0]+" "+str(doc[1]))
    f.write('--------------------------------------')
    for doc in model.most_similar(positive=['silnice', 'vlak'], negative=['kolej']):
        f.write(doc[0]+" "+str(doc[1]))
    f.write('--------------------------------------')

    f.write(model.doesnt_match("bratr sestra auto strýc".split()))
    f.close()
