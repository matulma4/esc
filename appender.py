import numpy as np

class MySentences:
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
    data = MySentences("base_text_features.rtData")
    features = []
    max_ftr = 0
    for line in data:
        parsed_row = line.strip().split("#", 1)
        data_array = parsed_row[0].split()
        metadata_array = parsed_row[1].split('\t')
        relevancy = data_array[0]
        qid = data_array[1].split(":")[1]
        query_text = metadata_array[0]
        hash_doc = metadata_array[2]
        doc_features = [ftr.split(":") for ftr in data_array[2:]]

        max_ftr = max(np.max([int(a[0]) for a in doc_features]),max_ftr)

        doc = DocRow(relevancy,qid,doc_features,metadata_array)
        features.append(doc)
    my_ftr = max_ftr + 1

    for i in range(len(features)):
        doc = features[i]
        doc.doc_features.append([str(my_ftr),str(147.2)])
        # features.append(parsed_row)
    print(max_ftr)
