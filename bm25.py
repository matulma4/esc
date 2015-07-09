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

def get_idf(corpus):
    result = {}
    N = len(corpus)
    for doc in corpus:
        for t_id, count in doc:
            if (t_id in result):
                result[t_id] += 1
            else:
                result[t_id] = 1
        
    result = dict([(name, compute_idf(val, N)) for name, val in result.items()])
    return result

def compute_idf(D,N):
    return math.log10((N-D+0.5)/(D+0.5))

def get_weights(query,tfidf_corp):
    result = []
    dot = 0
    i = 0
    for doc in tfidf_corp:
        for t_id,weight in doc:
            for q_id,count in query:
                if t_id == q_id:    
                    dot += weight*count
        result.append((i,(dot/(compute_norm(query)*compute_norm(doc)))))
        dot = 0
        i += 1
    return result

def compute_norm(vec):
    result = 0
    for key,elem in vec:
        result += elem*elem
    return math.sqrt(result)

def my_bm25(corpus,avglen,idf_data):
    result = []
    for doc in corpus:
        result.append([(t_id,compute_bm25(idf_data[t_id], freq, avglen, len(doc))) for t_id,freq in doc])
    return result

def compute_bm25(idf,tf,avglen,length):
    b = 0.75
    k1 = 1.6    
    return idf*(tf*(k1+1))/(tf+k1*(1 - b + b * (length/avglen)))

if __name__ == "__main__":
    #dataset = load_data('mycorpus.txt')
    #edited_data = edit_data(dataset)
    dataset = gutenberg.sents('carroll-alice.txt')
    edited_data = edit_data(dataset)    
    avg = 0
    for doc in edited_data:
        avg += len(doc)
    avg = avg/len(edited_data)
    
    dictionary = make_dict(edited_data)
    corpus = [dictionary.doc2bow(text) for text in edited_data]
    idf_data = get_idf(corpus)   
    
    mybm25 = my_bm25(corpus, avg, idf_data)
    query = raw_input('Enter query: ')
    porter = PorterStemmer()
    query = [porter.stem(word) for word in query.lower().split()]
    new_vec = dictionary.doc2bow(query)    
    
    weights = get_weights(new_vec, mybm25)
    sorted_weights = sorted(weights, key=operator.itemgetter(1),reverse=True)    
    
    i = 0
    for key,value in sorted_weights:
        if (value == 0) or (i == 5):
            break
        for doc in dataset[key]:
            print(unicode(doc)),
        print('')
        i += 1
    print('End of output ')    