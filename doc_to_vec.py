from gensim import models
import numpy as np
from sklearn.manifold import TSNE
# from w2vg import MySentences
import matplotlib.pyplot as plt
from bokeh.plotting import figure,output_file,show
from basicgrad import q
from train import train



def average_vec(mx,model,length):
    """Accepts list of words and word2vec model. Returns average of vectors of the words"""

    count = len(mx)
    vec_sum = np.zeros(length)
    return vec_sum
    # for vec in mx:
    #     # print vec
    #     if vec in model.vocab.keys():
    #         vec_sum += model[vec]
    #     # else:
    #     #     print("Word "+vec+" not in vocabulary")
    # return vec_sum/count

class MyWords:
    def __init__(self,model):
        self.model = model

    def __iter__(self):
        for word in self.model.vocab.keys():
            yield model[word]

def visualize(model):
    output_file("ffs.html")
    X = [model[word][0] for word in model.vocab.keys()]
    Y = [model[word][1] for word in model.vocab.keys()]
    # p = figure(plot_width=1280,plot_height=720)
    # # p.scatter(X[:100],Y[:100],marker="circle")
    # labels = [word.decode('utf-8') for word in model.vocab.keys()]
    # for label, x, y in zip(labels[20000:20500], X[20000:20500], Y[20000:20500]):
    #     p.text(float(x),float(y),text=[label],text_font_size="10pt")
    # show(p)
    # plt.scatter(X, Y, alpha=0.5)
    # plt.plot(X,Y, 'k.', markersize=0.5)
    labels = [word.decode('utf-8') for word in model.vocab.keys()]
    for label, x, y in zip(labels, X, Y):
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
    docs = [line.split() for line in open("content.raw_text")]
    d = []
    for doc in docs:
        d.append(average_vec(doc,model,length))
    for line in open("base_text_features.rtData"):
        words = line.split()
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
        q_vec = average_vec(query,model,length)
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
    fname = "content.word2vec"
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