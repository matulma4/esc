#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import random
import glob
import pickle
import os.path

from gensim import models
import numpy as np
from joblib import Parallel,delayed
from scipy import io

from basicgrad import q
from logreg import train


class Doc_Model():
    def __init__(self,M,b):
        self.M = M
        self.b = b

class Questions():
    def __init__(self,q):
        self.q = q

def mean(a):
    return sum(a) / len(a)

def average_vec(mx,model,length):
    """Accepts list of words and word2vec model. Returns average of vectors of the words"""

    vec = np.matrix([model[word] for word in mx if word in model.vocab.keys()])
    if not vec.any():
        vec =[[np.zeros(length)]]
    return np.mean(vec,0)
    # return sum(vec)/len(vec)
    # return map(mean,zip(*vec))


class MySentences:
    def __init__(self,fname):
        self.fname = fname
        self.i = 0
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        self.length = i+1

    def __iter__(self):
        with open(self.fname) as f:
            for line in f:
                # print self.i
                self.i += 1
                yield line

    def __len__(self):
        return self.length

    def __getitem__(self, item):
        with open(self.fname) as f:
            for i, l in enumerate(f):
                if i == item:
                    return l.split()



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
    dictionary = load_doc_hashes("temp_mapper.txt")
    questions = {}
    # dim = len(model[model.vocab.keys()[0]])
    # docs = [line.split() for line in open("content.raw_text")]
    # docs = MySentences("temp_new.raw_text")
    # length = len(docs)
    dim = len(model[model.vocab.keys()[0]])
    d = MySentences("new_averages.txt")# io.mmread("R_new.mtx").T # [average_vec(mx,model,dim) for mx in docs]
    features = MySentences("temp_features.rtData")
    length = len(d)
    queries = {}
    o = 0
    for words in features:
        o += 1
        if o == 2000:
           break
        # words = line.split()
        relevancy = int(words[0])/5
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

        if qid in queries.keys():
            q_vec = queries[qid]
        else:
            q_vec = average_vec(query,model,dim)
            queries[qid] = q_vec
        index = translate_hash(hash,dictionary)
        if index > -1 and index < length:
            # document = docs[index]
            # doc_vec = average_vec(document,model,length)
            if qid in questions.keys():
                new = np.array([np.array([float(a) for a in d[index]])]).T
                questions[qid].a = np.hstack((new,questions[qid].a))
                # questions[qid].atext.insert(0,document)
                questions[qid].y = np.append(questions[qid].y,relevancy)
            else:
                # print q_vec,[float(a) for a in d[index]],query,[document],np.array([])
                questions[qid] = q(q_vec,[float(a) for a in d[index]],relevancy)
    return questions

def parse_feature_line(line):
    halves = line.split(' #')
    ftr = halves[0].split()
    metadata = halves[1].split('\t')
    relevancy = int(ftr[0])
    qid = int(ftr[1].split(':')[1])
    query = metadata[0].strip()
    if len(metadata) < 3:
        print line
    hash = metadata[2]
    return (relevancy,qid,query,hash)

def load_questions(model,rel,hash,qid,dictionary):
    # features = [line for line in open(fname)]
    questions = {}
    # length = len(model.docvecs)
    for i in range(len(rel)):
        qi = qid[i]
        r = rel[i]
        h = hash[i]
        index = translate_hash(h,dictionary)
        # if qid in queries.keys():
        #     q_vec = queries[qid]
        # else:
        #     q_vec = average_vec(query,model,dim)
        #     queries[qid] = q_vec
        q_vec = [int(a) for a in '{:020b}'.format(int(qi))]*5
        if index > -1: # and index < length:
            if qi in questions.keys():
                new = np.array([np.array([float(a) for a in model.docvecs[index]])]).T
                questions[qi].a = np.hstack((new,questions[qi].a))
                questions[qi].y = np.append(r,questions[qi].y)
            else:
                questions[qi] = q(q_vec,[float(a) for a in model.docvecs[index]],r)
    return questions

def merge_dicts(dicts):
    questions = dicts[0]
    for i in range(1,len(dicts)):
        dictionary = dicts[i]
        for qid in dictionary.keys:
            value = dictionary[qid]
            if qid in questions.keys():
                questions[qid].a = np.hstack((value.a,questions[qid].a))
                questions[qid].y = value.y[::-1] + questions[qid].y# np.append(questions[qid].y,relevancy)
            else:
                questions[qid] = value
                questions[qid].y = questions[qid].y[::-1]
    return questions


def load_thread(n_processors,feature_dataset_dir):
    # d = io.mmread("R_new.mtx").T
    model = models.Doc2Vec.load("model1.doc2vec")
    dictionary = load_doc_hashes("doc_mapper.txt")
    dim = len(model.docvecs[0])
    questions = {}
    files = sorted(glob.glob(feature_dataset_dir + "/feature_*"))
    results = Parallel(n_jobs=n_processors)(delayed(load_questions)(fname,questions,dictionary,model,dim) for fname in files)
    with open("backup.pickle","wb") as f:
        o = Questions(results)
        pickle.dump(o,f)
    return questions

def dummy_file(length,dim):
    random.seed(13)
    with open("dummy_averages.txt","w") as f:
        for i in range(length):
            for j in range(dim):
                f.write(str(random.randrange(100)) + " ")
            f.write("\n")

def matrix_to_file():
    csc = io.mmread("R_new.mtx")
    R = csc.T
    with open("new_averages.txt","w") as f:
        for line in R:
            for value in line:
                f.write(str(value)+" ")
            f.write("\n")

if __name__ == "__mein__":

    if os.path.isfile("questions_content.pickle"):
        with open("questions_content.pickle") as f:
            questions = pickle.load(f)
    else:

        # io.mmread("R_new.mtx")
        # model = models.Word2Vec.load("model6.word2vec")
        # dictionary = load_doc_hashes("temp_mapper.txt")
        # dim = len(model[model.vocab.keys()[0]])
        # d = np.zeros(shape=(10000,100))
        questions = load_thread(16,os.getcwd())
        qs = Questions(questions)
        with open("correct_questions_content.pickle","wb") as f:
            pickle.dump(qs,f)




if __name__ == "__muin__":
    with open("pickle/questions_content.pickle") as f:
            questions = pickle.load(f)
    (M,b) = train(questions.q.values(),[])
    doc_model = Doc_Model(M,b)
    with open("doc_model_content.pickle","wb") as f:
        pickle.dump(doc_model,f)
    # new_questions = merge_dicts(questions.q)
    # qs = Questions(new_questions)
    # with open("new_questions_content.pickle","wb") as f:
    #     pickle.dump(qs,f)

if __name__ == "__main__":
    rel = [line for line in open("rel4.txt")]
    hash = [line for line in open("hashes2.txt")]
    qid = [line for line in open("metadata2.txt")]
    dictionary = load_doc_hashes("doc_mapper.txt")
    model = models.Doc2Vec.load("model1.doc2vec")
    questions = load_questions(model,rel,hash,qid,dictionary)
    with open("doc2vec_questions.pickle","w") as f:
        pickle.dump(questions,f)
