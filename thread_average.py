#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
from gensim import models
import numpy as np
import io

def average(lines, result, model, dim):
    length = len(lines)
    for i in range(length):
        line = lines[i]
        vec = np.matrix([model[word] for word in line if word in model.vocab.keys()])
        if not vec.any():
            result[i] = np.zeros(dim)
        else:
            result[i] = np.mean(vec,0)




if __name__ == "__main__":
    threads = []
    n = 16
    model = models.Word2Vec.load("model5.word2vec")
    lines = [line.split() for line in open("temp.raw_text")]
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

    with open("averages.txt",'w') as f:
        for vec in result:
            for value in vec:
                f.write(str(value)+" ")
            f.write('\n')