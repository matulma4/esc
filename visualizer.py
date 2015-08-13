import matplotlib.pyplot as plt
from bokeh.plotting import figure,output_file,show
from gensim import models
import numpy as np

def dist(x,y):
    return np.sqrt(x*x+y*y)


def visualize(model):
    X = [model[word][0] for word in model.vocab.keys()]
    Y = [model[word][1] for word in model.vocab.keys()]
    segments = [[] for seg in range(16)]
    labels = [word.decode('utf-8') for word in model.vocab.keys()]
    for x,y,label in zip(X,Y,labels):
        distance = dist(x,y)
        i = 0
        e = 0.02
        while distance > e:
            i += 1
            e += 0.02
            if i == 15:
                break
        segments[i].append((x,y,label))
    for i in range(16):
        plt.figure(i)
        seg = segments[i]
        for x, y,label in seg:
            plt.annotate(label,(x, y))
    plt.show()


if __name__ == "__main__":
    model = models.Word2Vec.load("model5.word2vec")
    visualize(model)