import numpy as np
from gensim.models import Doc2Vec
import os
class QATuple():
    def __init__(self,q,dplus,dminus):
        self.q = q
        self.plus = dplus
        self.minus = dminus

class Answer():
    def __init__(self,url,vec,rel):
        self.url = url
        self.vec = np.matrix(vec).T
        self.rel = rel
    def __lt__(self, other):
        return self.rel < other.rel

class Question():
    def __init__(self,qi,ans,qtext,qvec):
        self.q = qi #np.matrix(np.ones(12)).T#np.matrix([int(c) for c in '{:012b}'.format(int(qi))]).T
        self.a = ans
        self.qtext = qtext
        self.qvec = qvec

def load_question(fname,vecs,qid_dict,doc_dict,a_model):
    answers = []
    for line in open(fname):
        halves = line.split('#')
        signals = halves[0].split()
        rel = int(signals[0])
        # sigs = [float(a.split(':')[1]) for a in signals[2:]]
        metadata = halves[1].strip().split(' ')
        url = metadata[1]
        hash = metadata[2]
        answers.append(Answer(url,a_model.doctag_syn0[doc_dict[hash]],rel))
    qtext = metadata[0]
    qid = int(signals[1].split(':')[1])
    answers.sort()
    answers = answers[-1:0:-1]
    return Question(qid,answers,qtext,vecs[qid_dict[qid]])

def create_tuples(question):
    tuples = []
    l = len(question.a)
    for i in range(l):
        answer = question.a[i]
        for j in range(i+1,l):
            ans = question.a[j]
            if answer.rel > ans.rel:
                tuples.append(QATuple(question.q,answer.vec,ans.vec))
    return tuples
def load_questions(modelname,f_name,mapname,a_modelname):
    model = Doc2Vec.load(modelname)
    a_model = Doc2Vec.load(a_modelname)
    qids = list(enumerate([int(q) for q in open(f_name)]))
    rev_qids = [(item,index) for index,item in qids]
    qid_dict = dict(rev_qids)
    Q = []
    doc_dict = load_doc_hashes(mapname)
    for fname in os.listdir("questions"):
        Q.append(load_question("questions/"+fname,model.docvecs.doctag_syn0,qid_dict,doc_dict,a_model))
    return Q

def load_tuples(questions):
    t = []
    for q in questions:
        t = t + create_tuples(q)
    return t


def load_doc_hashes(mapper_file):
    hash_list = {}
    with open(mapper_file,'r') as mapper_f:
        for line, row in enumerate(mapper_f):
            hash_list[row.strip()] = line
    return hash_list
