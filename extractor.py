__author__ = 'Martin'


from doc_to_vec import load_doc_hashes
from doc_to_vec import MySentences

class MyWords(MySentences):
    def __init__(self,fname):
        self.fname = fname

    def __iter__(self):
        with open(self.fname) as f:
            for line in f:
                yield line

if __name__ == "__main__":
    features = MyWords("temp_features.rtData")
    documents = [line for line in open("content.raw_text")]
    docs = load_doc_hashes("doc_mapper.txt")
    rows = []
    for row in features:
        parse_row = row.split("#",1)
        metadata_array = parse_row[1].strip().split('\t')
        qid = parse_row[0].strip().split(':', 1)[1].split(' ',1)[0]
        hash = metadata_array[2]
        rows.append(documents[docs[hash]])
    with open("temp_all.raw_text","w") as f:
        for r in rows:
            f.write(r)
            f.write("\n")