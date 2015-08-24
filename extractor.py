__author__ = 'Martin'

from appender import MyWords
from doc_to_vec import load_doc_hashes

if __name__ == "__main__":
    features = MyWords("base_text_features.rtData")
    docs = load_doc_hashes("temp_mapper.txt")
    rows = []
    for row in features:
        parse_row = row.split("#",1)
        metadata_array = parse_row[1].strip().split('\t')
        qid = parse_row[0].strip().split(':', 1)[1].split(' ',1)[0]
        hash = metadata_array[2]
        if hash in docs.keys():
            rows.append(row)
    with open("temp_features.rtData","w") as f:
        for r in rows:
            f.write(row)
            f.write("\n")