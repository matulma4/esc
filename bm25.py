from gensim import corpora, models, similarities
from collections import defaultdict
from nltk.stem.porter import PorterStemmer
from nltk.corpus import gutenberg
import operator
import math

def load_data(datafile):
    return [line for line in open(datafile)]

def edit_data(edited):
    #[line.lower().split() for line in dataset]
    ed = []
    for doc in edited:
        ed.append([term.lower() for term in doc])
    porter = PorterStemmer()
    result = []
    for line in ed:
        result.append([porter.stem(word) for word in line])
    return result

def make_dict(lines):
    stoplist = set('for a of the and to in by an as at'.split())
    dictionary = corpora.Dictionary(lines)
    
    stop_ids = [dictionary.token2id[stopword] for stopword in stoplist
                if stopword in dictionary.token2id]
    once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.items() if docfreq == 1]
    dictionary.filter_tokens(stop_ids + once_ids) 
    dictionary.compactify() 
    return dictionary

def get_idf(corpus, query):
    result = {}
    N = len(corpus)
    for q,c in query:
        for doc in corpus:
            for t_id, count in doc:
                if q == t_id:
                    if q in result:
                        result[q] += 1
                    else:
                        result[q] = 1
                    break;
    for q in result.keys():
        result[q] = compute_idf(result[q],N)

    return result

def compute_idf(D,N):
    return math.log10((N-D+0.5)/(D+0.5))
    # return math.log(N/D,2)

def get_weights(query,tfidf_corp):
    result = []
    i = 0
    for doc in tfidf_corp:
        dot = 0
        for t_id,weight in doc:
            for q_id,count in query:
                if t_id == q_id:    
                    dot += weight*count
        norm = compute_norm(query)*compute_norm(doc)
        if norm == 0:
            norm = 1
        result.append((i, (dot/norm)))
        i += 1
    return result

def compute_norm(vec):
    result = 0
    for key,elem in vec:
        result += elem*elem
    return math.sqrt(result)

def my_bm25(corpus, avglen, idf_data):
    result = []
    i = 0
    for doc in corpus:
        # print(doc)
        total = 0
        for q in idf_data.keys():
            for t_id,freq in doc:
                if t_id == q:
                    total += compute_bm25(idf_data[q], freq, avglen, len(doc))
        result.append((i, total))
        i += 1;
    return result

def compute_bm25(idf,tf,avglen,length):
    b = 0.75
    k1 = 1.6
    # k3 = 1.6
    result = idf*((tf*(k1+1))/(tf+k1*(1 - b + b * (length/avglen))))
    # print(result)
    return result # *((k3 + 1)* tf/(k3 + tf))

if __name__ == "__main__":
    # dataset = load_data('mycorpus.txt')
    # edited_data = edit_data(dataset)
    dataset = gutenberg.sents('milton-paradise.txt')
    edited_data = edit_data(dataset)    
    avg = 0
    for doc in edited_data:
        avg += len(doc)
    avg = avg/len(edited_data)
    
    dictionary = make_dict(edited_data)
    corpus = [dictionary.doc2bow(text) for text in edited_data]

    query = raw_input('Enter query: ')
    porter = PorterStemmer()
    query = [porter.stem(word) for word in query.lower().split()]
    new_vec = dictionary.doc2bow(query)
    # print(new_vec)
    idf_data = get_idf(corpus,new_vec)
    mybm25 = my_bm25(corpus, avg, idf_data)

    sorted_weights = sorted(mybm25, key=operator.itemgetter(1),reverse=True)
    i = 0
    for key,value in sorted_weights:
        if (value == 0) or (i == 5):
            break
        for doc in dataset[key]:
            print(unicode(doc)),
        print('')
        i += 1
    print('End of output ')    