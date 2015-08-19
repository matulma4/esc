#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
from gensim import models
import numpy as np
from joblib import Parallel,delayed
import glob,os


def average(f,model):
    dim = len(model[model.vocab.keys()[0]])
    lines = [line.split() for line in open(f)]
    length = len(lines)
    result = np.empty(shape=(length,dim))
    for i in range(length):
        line = lines[i]
        vec = np.matrix([model[word] for word in line if word in model.vocab.keys()])
        if not vec.any():
            result[i] = np.zeros(dim)
        else:
            result[i] = np.mean(vec,0)

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


    # merge_temp_file(output)


if __name__ == "__main__":
    model = models.Word2Vec.load("model5.word2vec")
    average_documents(os.getcwd()+"\chunks",4,model)
    # threads = []
    # n = 16
    # model = models.Word2Vec.load("content.word2vec")
    # lines = [line.split() for line in open("content.raw_text")]
    # length = len(lines)
    # dim = len(model[model.vocab.keys()[0]])
    # result = np.empty(shape=(length,dim))
    # size = length/(n-1)
    #
    # for i in range(0,length,size):
    #     t = threading.Thread(target=average,args=(lines[i:i+size],result[i:i+size],model,dim,))
    #     threads.append(t)
    #     t.start()
    # for thread in threads:
    #     thread.join()
    #
    # with open("averages_content.txt",'w') as f:
    #     for vec in result:
    #         for value in vec:
    #             f.write(str(value)+" ")
    #         f.write('\n')