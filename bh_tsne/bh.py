from gensim import models
# import numpy as np
import argparse,os

def convert_data(fname):
    model = models.Word2Vec.load(fname)
    dim = len(model.syn0[0])
    n = len(model.syn0)
    limit = 10000
    for a in range(103):
        i = 0
        with open("data"+os.sep+"data"+str(a)+".txt","wb") as f:
            if a == 102:
                f.write(str(n - 1020000)+" "+str(dim)+"\n")
            else:
                f.write(str(limit)+" "+str(dim)+"\n")
            for vec in model.syn0:
                if i == limit:
                    break
                for value in vec:
                    f.write(str(value) + " "),
                f.write("\n")
                i += 1




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converts data")
    parser.add_argument("filename",help="model file",type=str)
    args = parser.parse_args()
    convert_data(args.filename)
    # get_result("result.dat")
