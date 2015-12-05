import pickle
from doc_to_vec import MySentences

class MyWords(MySentences):
    def __init__(self,fname):
        self.fname = fname

    def __iter__(self):
        with open(self.fname) as f:
            for line in f:
                yield line

class DocRow:
    def __init__(self,relevancy,id,doc_features,metadata):
        self.relevancy = relevancy
        self.id = id
        self.doc_features = doc_features
        self.metadata = metadata

if __name__ == "__main__":
    data = MySentences("../base_text_features.rtData")
    # with open("signals.pickle") as f:
    #     signals = pickle.load(f)
    signals = [int(sig) for sig in open("rel7.txt")]
    features = []
    max_ftr = 926
    g = open("new_text_features6.rtData","w")
    i = 0
    for line in data:
        halves = line.split('#')
        ftr = float(signals[i])
        new_line = halves[0]+" "+str(max_ftr)+":"+str(ftr)+" #"+halves[1]+"\n"
        g.write(new_line)
        i += 1
    g.close()
