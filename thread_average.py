#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
from gensim import models,corpora,matutils
import numpy as np
from joblib import Parallel,delayed
import glob,os
from doc_to_vec import MySentences


def average(f,model):
    dim = len(model[model.vocab.keys()[0]])
    lines = MySentences(f) # [line.split() for line in open(f)]
    length = len(lines)
    result = np.empty(shape=(length,dim))
    i = 0
    for line in lines:
        # line = lines[i]
        vec = np.matrix([model[word] for word in line if word in model.vocab.keys()])
        if not vec.any():
            result[i] = np.zeros(dim)
        else:
            result[i] = np.mean(vec,0)
        i += 1

    with open(f+".out","w") as f:
        for res in result:
            for value in res:
                f.write(str(value)+" ")
            print("\n")

def average_documents(feature_dataset_dir, n_processors,model):
    """
    Load texts from Seznam protobuffer to memory
    :return: structure of text + doc_hash
    """
    files = sorted(glob.glob(feature_dataset_dir + "/document_*"))

    results = Parallel(n_jobs=n_processors)(delayed(average)(f, model) for f in files)


def threading_old():
    threads = []
    n = 16
    model = models.Word2Vec.load("content.word2vec")
    lines = [line.split() for line in open("content.raw_text")]
    length = len(lines)
    dim = len(model[model.vocab.keys()[0]])
    result = np.empty(shape=(length,dim))
    size = length/(n-1)
    for i in range(0,length,size):
        t = threading.Thread(target=average,args=(lines[i:i+size],result[i:i+size],model,dim,))
        threads.append(t)
        t.start()
    for thread in threads:
        thread.join()

    with open("averages_content.txt",'w') as f:
        for vec in result:
            for value in vec:
                f.write(str(value)+" ")
            f.write('\n')

def load_d(fname):
    with open(fname) as f:
        for line in f:
            yield f.split()

def doc2bow(doc,dictionary):
    dictio = {}
    for word in doc:
        print word
        if word not in dictionary.keys():
            continue
        num = dictionary[word].index
        if num in dictio.keys():
           dictio[num] += 1
        else:
           dictio[num] = 1
    return [(w_id,dictio[w_id]) for w_id in dictio.keys()]

def convert_to_corpus(model_name,fname):
    model = models.Word2Vec.load(model_name)
    # sentences = load_d(fname)
    docs = [line.split() for line in open(fname)]
    dictionary = corpora.Dictionary(docs)
    dictionary.doc2bow()
    corpus = [doc2bow(text,model.vocab) for text in docs]
    csc = matutils.corpus2csc(corpus)
    return csc

if __name__ == "__main__":
    csc = convert_to_corpus("model5.word2vec","temp.raw_text")
    print csc
    # parser = argparse.ArgumentParser(description="Compute document averages of word vectors.")
    # parser.add_argument("n_processors",help="number of processors used",type=int)
    # parser.add_argument("filename",help="model file",type=str)
    # args = parser.parse_args()
    # model = models.Word2Vec.load(args.filename)
    # average_documents(os.getcwd()+"/chunks",args.n_processors,model)
