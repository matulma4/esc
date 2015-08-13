from gensim import models
import numpy as np
# from sklearn.manifold import TSNE
# from w2vg import MySentences
# import matplotlib.pyplot as plt
# from bokeh.plotting import figure,output_file,show
from basicgrad import q
# from train import train



def average_vec(mx,model):
    """Accepts list of words and word2vec model. Returns average of vectors of the words"""

    vec = np.matrix([model[word] for word in mx])
    return np.mean(vec)
    # for vec in mx:
    #     # print vec
    #     if vec in model.vocab.keys():
    #         vec_sum += model[vec]
    #     # else:
    #     #     print("Word "+vec+" not in vocabulary")
    # return vec_sum/count

class MySentences:
    def __init__(self,fname):
        self.fname = fname
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        self.length = i+1

    def __iter__(self):
        for line in open(self.fname):
            yield line.split()

    def __len__(self):
        return self.length

    def __getitem__(self, item):
        with open(self.fname) as f:
            for i, l in enumerate(f):
                if i == item:
                    return l


def visualize(model):
    X = [model[word][0] for word in model.vocab.keys()]
    Y = [model[word][1] for word in model.vocab.keys()]
    segments = [[] for seg in range(15)]
    labels = [word.decode('utf-8') for word in model.vocab.keys()]
    for x,y,label in zip(X,Y,labels):
        if x < 0.1:
            if y < 0.1:
                segments[0].append((x,y,label))
            elif y < 0.2:
                segments[1].append((x,y,label))
            elif y < 0.3:
                segments[2].append((x,y,label))
        elif x < 0.2:
            if y < 0.1:
                segments[3].append((x,y,label))
            elif y < 0.2:
                segments[4].append((x,y,label))
            elif y < 0.3:
                segments[5].append((x,y,label))
        elif x < 0.3:
            if y < 0.1:
                segments[6].append((x,y,label))
            elif y < 0.2:
                segments[7].append((x,y,label))
            elif y < 0.3:
                segments[8].append((x,y,label))
        elif x < 0.4:
            if y < 0.1:
                segments[9].append((x,y,label))
            elif y < 0.2:
                segments[10].append((x,y,label))
            elif y < 0.3:
                segments[11].append((x,y,label))
        elif x < 0.5:
            if y < 0.1:
                segments[12].append((x,y,label))
            elif y < 0.2:
                segments[13].append((x,y,label))
            elif y < 0.3:
                segments[14].append((x,y,label))
    for i in range(15):
        # output_file("bokeh\\"+str(i)+".html")
        # p = figure(plot_width=800,plot_height=600)
        seg = segments[i]
        # p.scatter(X[:100],Y[:100],marker="circle")
        # labels = [word.decode('utf-8') for word in model.vocab.keys()]
        for x, y, label in seg:
            # p.text(float(x),float(y),text=[label],text_font_size="10pt")
            pass
        # show(p)

    # plt.scatter(X, Y, alpha=0.5)
    # plt.plot(X,Y, 'k.', markersize=0.5)

    #     plt.figure(i)
    #     seg = segments[i]
    #     for x, y,label in seg:
    #         plt.annotate(label,(x, y))
    # plt.show()

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

def load_doc_hashes(mapper_file):
    hash_list = {}
    with open(mapper_file,'r') as mapper_f:
        for line, row in enumerate(mapper_f):
            hash_list[row.strip()] = line
    return hash_list

def translate_hash(hash,dictionary):
    if hash in dictionary.keys():
        return dictionary[hash]
    else:
        return -1

def load_qs(model):
    dictionary = load_doc_hashes("doc_mapper.txt")
    questions = {}
    length = len(model[model.vocab.keys()[0]])
    # docs = [line.split() for line in open("content.raw_text")]
    docs = MySentences("content.raw_text")
    d = []
    for doc in docs:
        d.append(average_vec(doc,model))
    features = MySentences("base_text_features.rtData")
    for words in features:
        # words = line.split()
        relevancy = int(words[0])
        qid = int(words[1].split(':')[1])
        # query = words[:x]
        i = 2
        while words[i] != "#":
            i += 1
        i += 1
        query = []
        while words[i][0:4] != "http":
            query.append(words[i])
            i += 1
        url = words[i]
        hash = words[i+1]
        q_vec = average_vec(query,model)
        # connected_docs = words[x:]
        index = translate_hash(hash,dictionary)
        if(index > -1 and index < len(docs)):
            document = docs[index]
            # doc_vec = average_vec(document,model,length)
            if qid in questions.keys():
                questions[qid].a = np.hstack((np.array([d[index]]).T,questions[qid].a))
                questions[qid].atext.insert(0,document)
                questions[qid].y = np.insert(questions[qid].y,0,1)
            else:
                questions[qid] = q(q_vec,[d[index]],np.empty((1,2)),query,[document],np.array([]))
    return questions

if __name__ == "__main__":
    fname = "model5.word2vec"
    # fname = sys.argv[1]
    model = models.Word2Vec.load(fname)


    # output_tsne(model)
    # visualize(model)
    questions = load_qs(model)
    # (M,b) = train(questions.values(),[])
    for q in questions:
        print len(q.a)

    # data_name = 'temp.raw_text'
    # sentences = MySentences(data_name)
    # i = 0
    # d = []
    #
    # for sent in sentences:
    #     d.append(average_vec(sent,model,length))
    # # query = raw_input("Enter query: ").split()
    # # print(average_vec(query,model))
    # print ""