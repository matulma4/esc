from doc_to_vec import parse_feature_line,load_doc_hashes,translate_hash,Doc_Model,average_vec
import pickle,os,glob
from gensim import models
from scipy import io
import numpy as np
from joblib import Parallel,delayed

def transform_to_signal(fname,queries,dictionary,M,b,model,dim,R):
    result = []
    lines = [line for line in open(fname)]
    for line in lines:
        (relevancy,qid,query,hash) = parse_feature_line(line)
        index = translate_hash(hash,dictionary)
        if qid in queries.keys():
            q_vec = queries[qid]
        else:
            q_vec = average_vec(query,model,dim)
            queries[qid] = q_vec
        doc_vec = np.array([R[index]]).T
        v = np.dot(q_vec,M)
        e = np.dot(v,doc_vec) + b
        # print(e)
        result.append(e.item(0))
    return result

def transform_thread(n_processors):
    queries = {}
    dictionary = load_doc_hashes("doc_mapper.txt")
    with open("doc_model2.pickle") as f:
        doc_model = pickle.load(f)
    M = doc_model.M
    b = doc_model.b
    model = models.Word2Vec.load("content.word2vec")
    dim = len(model[model.vocab.keys()[0]])
    R = io.mmread("R_old.mtx").T
    files = sorted(glob.glob(os.getcwd() + "/feature_*"))
    signals = Parallel(n_jobs=n_processors)(delayed(transform_to_signal)(fname,queries,dictionary,M,b,model,dim,R) for fname in files)
    return signals

if __name__ == "__main__":
    signals = transform_thread(16)
    pickle.dump(signals, open("signals.pickle", "wb"))
