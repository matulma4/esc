__author__ = 'Martin'

from appender import MyWords
from doc_to_vec import load_doc_hashes

if __name__ == "__main__":
    features = MyWords("temp_features.rtData")
    documents = MyWords("content.raw_text")
    docs = load_doc_hashes("doc_mapper.txt")
    rows = []
    for row in features:
        parse_row = row.split("#",1)
        metadata_array = parse_row[1].strip().split('\t')
        qid = parse_row[0].strip().split(':', 1)[1].split(' ',1)[0]
        hash = metadata_array[2]
        rows.append(documents[docs[hash]])
    with open("temp_features.rtData","w") as f:
        for r in rows:
            f.write(r)
            f.write("\n")