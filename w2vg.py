# Word2Vec gensim
import os.path

from gensim import models
# from nltk.corpus import gutenberg
import logging
def load_data(fname):
    return [line for line in open(fname) if line[0] != ':']
if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    fname = "model.doc2vec"
    if os.path.isfile(fname):
        model = models.Doc2Vec.load()
    else:
        dataset = load_data('questions-words.txt')
        dataset = [line.split() for line in dataset]
        model = models.Word2Vec(dataset, size=100, window=5, min_count=5, workers=4)
        model.save(fname)
    # model.init_sims(replace=True)
    for word,value in model.most_similar(positive=['woman', 'king'], negative=['man']):
        print(unicode(word)+' '+str(value))
    print model.doesnt_match("breakfast cereal dinner lunch".split())