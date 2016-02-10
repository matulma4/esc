from gensim import models
from gensim.models.doc2vec import TaggedLineDocument
from os import path
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train doc2vec.")
    parser.add_argument("fname",help="filename",type=str)
    parser.add_argument("model",help="modelname",type=str)
    args = parser.parse_args()
    sentences = TaggedLineDocument(args.fname)
    outname = args.model+".doc2vec"
    if path.isfile(outname):
        model = models.Doc2Vec.load(outname)
    else:
        model = models.Doc2Vec(size=100, window=5, min_count=5,workers=4)
        model.build_vocab(sentences)
        model.train(sentences)
        model.save(outname)
    print ""
