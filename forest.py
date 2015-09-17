from sklearn.ensemble import RandomForestClassifier
from scipy import io
import pickle

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

if __name__ == "__main__":
    forest = RandomForestClassifier(verbose=1)
    hash_list = load_doc_hashes("doc_mapper.txt")
    doc_hashes = [hash for hash in open("hashes.txt")]
    relevances = [relevance for relevance in open("relevances.txt")]
    R = io.mmread("R_old.mtx").T
    X = []
    y = []
    for i in range(len(doc_hashes)):
        hash_index = translate_hash(doc_hashes[i],hash_list)
        relevance = relevances[i]
        vec = R[hash_index]
        X.append(vec)
        y.append(relevance)
    pickle.dump((X,y),open("Xy.pickle","wb"))
    trainX = X[:884724]
    trainy = y[:884724]
    testX = X[884724:]
    testy = y[884724:]
    forest.fit(trainX,trainy)
    with open("score.txt","w") as f:
        f.write(forest.score(testX,testy))

