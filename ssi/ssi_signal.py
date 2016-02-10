import pickle,numpy as np
from gensim.models import Doc2Vec

def load_doc_hashes(mapper_file):
    hash_list = {}
    with open(mapper_file,'r') as mapper_f:
        for line, row in enumerate(mapper_f):
            hash_list[row.strip()] = line
    return hash_list

if __name__ == "__main__":
    q_model = Doc2Vec.load("q_model2.doc2vec").docvecs.doctag_syn0
    model = Doc2Vec.load("model.doc2vec").docvecs.doctag_syn0
    ddict = load_doc_hashes("doc_mapper.txt")
    hashes = [line for line in open("hashes.txt")]
    qids = [line for line in open("qids.txt")]
    def_hash = hashes[0]
    with open("SSI.pickle") as f:
        W = pickle.load(f)
    with open("q_dict.pickle") as g:
        Q = pickle.load(g)
    i = 0
    for line in hashes:
        if ':' in line:
            print(np.dot(np.dot(q_model[Q[qids[i]]],W),np.transpose(model[ddict[def_hash]])))
        else:
            print(np.dot(np.dot(q_model[Q[qids[i]]],W),np.transpose(model[ddict[line]])))
        i = i + 1
