from gensim import models
import numpy as np

def convert_data(fname):
    model = models.Word2Vec.load(fname)
    dim = len(model.syn0[0])
    n = len(model.syn0)
    with open("data.txt","wb") as f:
        f.write(str(n)+" "+str(dim)+"\n")
        for vec in model.syn0:
            for value in vec:
                f.write(str(value) +" "),
            f.write("\n")


def get_result(fname):
    with open(fname,"r") as f:
        a = np.fromfile(f,dtype=np.uint32,count=2)
        n = a[0]
        d = a[1]
        b = np.fromfile(f,dtype=np.double)
        for i in range(int(n)):
            for j in range(int(d)):
                print b[i+j],
            print "\n"

if __name__ == "__main__":
    convert_data("content.word2vec")
    # get_result("result.dat")
