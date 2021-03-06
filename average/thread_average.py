#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
from gensim import models,corpora,matutils
import numpy as np
from scipy import io
from joblib import Parallel,delayed
import glob,os.path
import threading


def average(f,model):
    dim = len(model[model.vocab.keys()[0]])
    lines = [line.split() for line in open(f)]
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
            yield line

def doc2bow(doc,dictionary):
    dictio = {}
    for word in doc:
        # print word
        if word not in dictionary.keys():
            continue
        num = dictionary[word].index
        if num in dictio.keys():
           dictio[num] += 1
        else:
           dictio[num] = 1
    return [(w_id,dictio[w_id]) for w_id in dictio.keys()]

def data_to_dic(fname):
    docs = [line.split() for line in open(fname)]
    dictionary = corpora.Dictionary(docs)
    dictionary.save_as_text(fname.split('.')[0]+".dic")

def load_dic(fname):
    dictionary = corpora.Dictionary()
    dictionary = dictionary.load_from_text(fname.split('.')[0]+".dic")
    return dictionary

def edit_dic(fname):
    result = {}
    with open(fname) as f:
        for line in f:
            words = line.split()
            result[words[1]] = [words[0],words[2]]
    return result

def get_sparse(fname):
    short = fname.split('.')[0]

    # if not os.path.isfile(os.getcwd()+os.sep+short+".dic"):
    #     print "Creating dictionary"
    #     data_to_dic(fname)
    if not os.path.isfile(os.getcwd()+os.sep+short+"_sparse.mtx"):
        # print "Editing dictionary"
        # dictionary = edit_dic(short+".dic")
        # print "Filtering dictionary"
        # filter_dic(model,dictionary,"new.dic")
        # print "Loading dictionary"
        dct = corpora.Dictionary.load_from_text("dict_big.txt")
        texts = [line.split() for line in open(fname)]
        corpus = [dct.doc2bow(text) for text in texts]
        csc = matutils.corpus2csc(corpus)
        io.mmwrite(short+"_sparse.mtx",csc)
    else:
        csc = io.mmread(short+"_sparse.mtx")
    return csc

def filter_dic(model,vocab,dictionary,fname):

    with open(fname,"w") as f:
        for key in vocab:
            if key in dictionary.keys():
                f.write(str(model.vocab[key].index)+'\t'+key+'\t'+str(dictionary[key][1])+'\n')
            else:
                f.write(str(model.vocab[key].index)+'\t'+key+'\t'+str(0)+'\n')


def sparse_thread(n_processors):
    model = models.Word2Vec.load("content.word2vec")
    dictionary = corpora.Dictionary.load_from_text("content.dic")
    keyset = model.vocab.keys()
    results = Parallel(n_jobs=n_processors)(delayed(filter_dic)(model,keyset[i*32000:(i+1)*32000],dictionary,"dict"+str(i)+".txt") for i in range(32))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute document averages of word vectors.")
    parser.add_argument("dataname",help="dataset",type=str)
    parser.add_argument("modelname",help="model file",type=str)
    args = parser.parse_args()

    model = models.Word2Vec.load(args.modelname)

    # keyset = model.vocab.keys()[1024000:]
    # dictionary = corpora.Dictionary.load_from_text("content.dic")
    # filter_dic(model,keyset,dictionary,"dict32.txt")
    # sparse_thread(32)
    # print "Model loaded"
    # fname = args.dataname# "temp_new.raw_text"
    # data_to_dic(fname)
    # # model = models.Word2Vec.load("model6.word2vec")

    csc = get_sparse("content.raw_text")
    R = np.array(model.syn0.T * csc) / np.array([1 if value == 0 else value for value in csc.sum(axis=0).A1])
    io.mmwrite("R_new.mtx",R)


    # average_documents(os.getcwd()+"/chunks",args.n_processors,model)
