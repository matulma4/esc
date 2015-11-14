from logistic import ordinal_logistic_fit
import numpy as np
import argparse,pickle
from gensim import models
def compute_confmat(X,w):
    Y = []
    w = np.matrix(w)
    for x in X:
        Y.append((w*np.transpose(np.matrix(x)))[0,0])
    confmat = np.zeros((6,6))
    for i in range(len(y)):
        predict = int(float(Y[i])+0.5)
        label = y[i]
        confmat[predict][label] += 1
    print confmat

def features(fname):
    lines = [line for line in open(fname)]
    X = []
    y = []
    for l in lines:
        data = l.split('#')[0].split()
        y.append(int(data[0]))
        X.append([float(d.split(':')[1]) for d in data[3:]])
    return (X,y)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute ordinal logistic regression")
    parser.add_argument("fname",help="modelname",type=str)
    parser.add_argument("rel",help="relname",type=str)
    args = parser.parse_args()
    y = [int(line) for line in open(args.rel)]
    model = models.Doc2Vec.load(args.fname)
    X = model.docvecs
    (w,theta) = ordinal_logistic_fit(X,y,max_iter=1000)
    with open("regress.pickle","wb") as f:
        pickle.dump((w,theta))


