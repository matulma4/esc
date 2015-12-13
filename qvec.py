import pickle,numpy as np
from gensim.models import Word2Vec

def average_vec(qtext,model):
    vec = np.matrix([model[word] for word in qtext if word in model.vocab.keys()])
    if not vec.any():
        vec =[len(qtext)*[1/len(qtext)]]
    return np.mean(vec,0)



if __name__ == "__main__":
    qs = [line.strip().split() for line in open("qid_text_unique.txt")]
    model = Word2Vec.load("content.word2vec")
    Q = {}
    for q in qs:
        qid = int(q[0])
        qtext = q[1:]
        Q[qid] = average_vec(qtext,model)
    with open("QVecs.pickle","wb") as f:
        pickle.dump(Q,f)