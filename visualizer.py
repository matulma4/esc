import matplotlib.pyplot as plt
from bokeh.plotting import figure,output_file,show
from gensim import models
import numpy as np
from doc_to_vec import MySentences

def dist(a,b):
    return np.sqrt(np.sum([x*x for x in a-b]))


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

def split_to_segs(fname,model_name):
    model = models.Word2Vec.load(model_name)
    segments = []
    segments.append([])
    lines = MySentences(fname)
    index = 0
    for line in model.syn0:
        # print index
        if index == 0:
            index += 1
            continue
        segment = 0
        float_line = line#np.array([float(word) for word in line])
        if len(segments[segment]) == 0:
            segments[segment].append((float_line,model.vocab.keys()[index].decode('utf-8')))
        else:
            flt_line = segments[segment][0][0]
            # print dist(float_line,flt_line)
            while(dist(float_line,flt_line) > 0.05):
                segment += 1
                if segment == len(segments):
                    segments.append([])
                    break
                flt_line = segments[segment][0][0]
            # print dist(float_line,flt_line),segment,len(segments),flt_line,float_line
            segments[segment].append((float_line,model.vocab.keys()[index].decode('utf-8')))
        index += 1

    return segments

def visualize_file(fname,model_name):
    # model = models.Word2Vec.load(model_name)
    with open(fname) as f:
        lines = [line.split() for line in f]
        X = [float(line[0]) for line in lines[1:]]
        Y = [float(line[1]) for line in lines[1:]]
        (xmax,ymax,xmin,ymin) = find_max_min(X,Y)
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
    segs = split_to_segs("C:\Users\Martin\PycharmProjects\esc-s\words\lemmatized-p50-t0.8\out.txt","model5.word2vec")

    for i in [2,13]:
        seg = segs[i]
        print seg[0][0]
        plt.figure(i)
        for xy,label in seg:
            plt.annotate(label,(xy[0], xy[1]))
        # plt.show()
    print max(len(s) for s in segs)
    print min(len(s) for s in segs)
    print np.average([len(s) for s in segs])
    # p = ["10","20","30","40","50","60","80","100"]
    # t = ["0.2","0.4","0.6","0.8","1"]
    # m = ["classic","lemmatized"]
    # for perplex in p[7:8]:
    #     for theta in t[4:5]:
    #         for mode in m[1:2]:
    #             path = "words\\"+mode+"-p"+perplex+"-t"+theta+"\\"
    #             visualize_file(path+"out.txt",path+"words.txt")


