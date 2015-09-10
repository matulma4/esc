#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
from gensim import models
import numpy as np
# from sklearn.manifold import TSNE
# from w2vg import MySentences
from basicgrad import q
import random
from train import train
import pickle
from scipy import io

class Doc_Model():
    def __init__(self,M,b):
        self.M = M
        self.b = b

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
                yield line.split()

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
    dictionary = load_doc_hashes("doc_mapper.txt")
    questions = {}
    dim = len(model[model.vocab.keys()[0]])
    # docs = [line.split() for line in open("content.raw_text")]
    docs = MySentences("content.raw_text")
    length = len(docs)
    dummy_file(length,dim)
    dim = len(model[model.vocab.keys()[0]])
    dummy_file(length,dim)
    d = io.mmread("R_new.mtx").T# MySentences("new_averages.txt")# [average_vec(mx,model,dim) for mx in docs]
    features = MySentences("base_all_features.rtData")
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
            document = docs[index]
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

if __name__ == "__main__":
    # matrix_to_file()
    fname = "content.word2vec"
    # fname = sys.argv[1]
    model = models.Word2Vec.load(fname)

    # output_tsne(model)
    questions = load_qs(model)
    (M,b) = train(questions.values(),[])
    doc_model = Doc_Model(M,b)
    with open("doc_model_content.pickle","wb") as f:
        pickle.dump(doc_model,f)
