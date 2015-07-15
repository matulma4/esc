# Word2Vec gensim

from gensim import corpora,models,similarities
from nltk.corpus import gutenberg
import logging

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    dataset = gutenberg.sents('bible-kjv.txt')
        model = models.Doc2Vec(dataset, size=100, window=5, min_count=5, workers=4)
    # model.init_sims(replace=True)
    for word,value in model.most_similar(positive=['woman', 'king'], negative=['man']):
        print(unicode(word)+' '+str(value))