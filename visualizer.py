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

def output_tsne(model):
    # X = [model[word] for word in model.vocab.keys()]
    # tsne = TSNE(n_components=2,random_state=0)
    # a = tsne.fit_transform(X)
    f = open("HighCharts\examples\scatter\index2.htm",'w')
    g = open("HighCharts\examples\scatter\start.htm",'r')
    h = open("HighCharts\examples\scatter\end.htm",'r')

    for line in g:
        f.write(line)

    f.write("[")
    i = 0
    for word in model.vocab.keys():
    # for i in range(len(a)):
        if i == 5000:
            break
        i += 1
        values = ""
        for value in model[word]:
            values += str(value)+", "
        values = values[:len(values)-2]
        f.write("{name: '"+word+"',color: 'rgba(119, 152, 191, .5)',data: [["+values+"]]},")

    f.write("]")

    for line in h:
        f.write(line)
    f.close()

if __name__ == "__main__":
    model = models.Word2Vec.load("model5.word2vec")
    visualize(model)