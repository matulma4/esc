# Word2Vec gensim
import os.path

from gensim import models
import numpy as np
# from nltk.corpus import gutenberg
import logging
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
        if (sent_end > length):
            sent_end = length
        dataset.append(words[count:sent_end])
        count = sent_end
    return dataset
if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    fname = "bigmodel.doc2vec"
    if os.path.isfile(fname):
        model = models.Word2Vec.load(fname)
    else:
        dataset = load_data('text8')
        model = models.Word2Vec(dataset, size=100, window=5, min_count=5, workers=4)
        model.save(fname)

    print model.most_similar(positive=['woman', 'king'], negative=['man'])
    print model.most_similar(positive=['sheep', 'milk'], negative=['cow'])
    print model.most_similar(positive=['Paris', 'Spain'], negative=['Madrid'])
    print model.doesnt_match("Paris Berlin Japan Tokyo".split())
    print model.doesnt_match("dinner salad lunch breakfast".split())