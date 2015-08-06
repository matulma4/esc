from gensim import models
import numpy as np
from sklearn.manifold import TSNE
# from w2vg import MySentences

def average_vec(mx,model,length):
    """Accepts list of words and word2vec model. Returns average of vectors of the words"""
    count = len(mx)
    vec_sum = np.zeros(length)

    for vec in mx:
        # print vec
        if vec in model.vocab.keys():
            vec_sum += model[vec]
        else:
            print("Word "+vec+" not in vocabulary")
    return vec_sum/count

class MyWords():
    def __init__(self,model):
        self.model = model
    def __iter__(self):
        for word in self.model.vocab.keys():
            yield model[word]

if __name__ == "__main__":
    fname = "model4.word2vec"
    # fname = sys.argv[1]
    model = models.Word2Vec.load(fname)

    X = [model[word] for word in model.vocab.keys()]
    tsne = TSNE(n_components=2,random_state=0)
    a = tsne.fit_transform(X)
    print a

    # data_name = sys.argv[2]+'raw_text'
    # data_name = 'temp.raw_text'
    # sentences = MySentences(data_name)
    # i = 0
    # d = []
    # length = len(model[model.vocab.keys()[0]])
    # for sent in sentences:
    #     d.append(average_vec(sent,model,length))
    # # query = raw_input("Enter query: ").split()
    # # print(average_vec(query,model))
    # print ""