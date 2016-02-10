# -*- coding: utf-8 -*-
from gensim import models
import sys
import os

if __name__ == "__main__":
    linesep = os.linesep
    model = models.Word2Vec.load(sys.argv[1])
    f = open(sys.argv[1]+'.out','w')
    f.write(sys.argv[1]+linesep)
    f.write('okno'+linesep)
    for doc in model.most_similar(positive=['okno']):
        f.write(doc[0]+" "+str(doc[1])+linesep)
    f.write('--------------------------------------'+linesep)
    f.write('clovek'+linesep)
    for doc in model.most_similar(positive=['člověk']):
        f.write(doc[0]+" "+str(doc[1])+linesep)
    f.write('--------------------------------------'+linesep)
    f.write('auto'+linesep)
    for doc in model.most_similar(positive=['auto']):
        f.write(doc[0]+" "+str(doc[1])+linesep)
    f.write('--------------------------------------'+linesep)

    f.write(model.doesnt_match("bratr sestra auto strýc".split())+linesep)
    f.write(linesep)
    f.write(linesep)
    f.close()
