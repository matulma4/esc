import matplotlib.pyplot as plt
from bokeh.plotting import figure,output_file,show
from gensim import models
import numpy as np

def dist(x,y):
    return np.sqrt(x*x+y*y)


def visualize_model(fname):
    model = models.Word2Vec.load(fname)
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

def visualize_file(fname,model_name):
    # model = models.Word2Vec.load(model_name)
    with open(fname) as f:
        lines = [line.split() for line in f]
        X = [float(line[0]) for line in lines[1:]]
        Y = [float(line[1]) for line in lines[1:]]
        # (a,b,c,d) = find_max_min(X,Y)
        # x_diff = a - c
        # y_diff = b - d
        # t = (x_diff/16 + y_diff/16)/2
        # step =  np.round(t,decimals=0)
        # segments = [[] for seg in range(16)]
        # labels = [word.decode('utf-8') for word in open(model_name)]
        # for x,y,label in zip(X,Y,labels):
        #     distance = dist(x,y)
        #     i = 0
        #     e = step
        #     while distance > e:
        #         i += 1
        #         e += step
        #         if i == 15:
        #             break
        #     segments[i].append((x,y,label))
        # for i in range(16):
        #     plt.figure(i)
        #     seg = segments[i]
        # plt.figure()
        labels = [line.decode('utf8') for line in open(model_name)]
        plt.plot(X,Y,"ro")
        for x, y,label in zip(X,Y,labels):
            plt.annotate(label,(x, y))
        plt.show()

def find_max_min(X,Y):
    xmin = np.min(X)
    ymin = np.min(Y)
    xmax = np.max(X)
    ymax = np.max(Y)
    return (xmax,ymax,xmin,ymin)
if __name__ == "__main__":
    # visualize_model("model5.word2vec")
    p = ["10","20","30","40","50"]
    t = ["0.2","0.4","0.6","0.8","1"]
    m = ["classic","lemmatized"]
    for perplex in p[4:5]:
        for theta in t:
            for mode in m[1:2]:
                path = "words\\"+mode+"-p"+perplex+"-t"+theta+"\\"
                visualize_file(path+"out.txt",path+"words.txt")


