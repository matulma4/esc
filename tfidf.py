# -*- coding: utf-8 -*-
from gensim import corpora, models, similarities
from collections import defaultdict
from nltk.stem.porter import PorterStemmer
from nltk.corpus import gutenberg
import operator
import math

def get_key(value,dic):
    for key in dic:
        if dic[key] == value:
            return key
    return -1

# def load_data(datafile):
#     return # [line for line in open(datafile)]

def edit_data(edited):
    # [line.lower().split() for line in dataset]
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

def my_make_dict(lines):
    result = {}
    freq = {}
    i = 0
    stoplist = set('for a of the and to in by an as at'.split())
    for line in lines:
        for term in line:   
            if not(term in stoplist):
                if(term in freq.keys()):
                    freq[term] += 1
                else:
                    freq[term] = 1
    for term in freq:
        if(freq[term] > 1):
            result[i] = term
            i += 1
    return result

def my_corpus(dictionary,dataset):
    result = []
    for line in dataset:
        tmp = {}
        for term in line:
            if (term in tmp.keys()):
                tmp[term] += 1
            else:
                tmp[term] = 1
        temp = []
        for value in tmp:
            a = get_key(value, dictionary)
            if(a > -1):
                temp.append((a,tmp[value]))
        result.append(temp)
    return result 

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

def get_freq(corpus,orig_set):
    result = []
    i = 0
    for line in corpus:
        l = len(orig_set[i])
        result.append([(t_id,freq) for t_id,freq in line])
        i += 1
    return result

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
    # print(math.log2(N/D))
    return math.log2(N/D)

def my_tfidf(idf_data,tf_data):
    result = []
    for line in tf_data:
        result.append([(t_id,freq*idf_data[t_id]) for t_id, freq in line])
    return result

def proc_query(query,dictionary):
    new_q = [get_key(value, dictionary) for value in query]
    result = {}
    for term in new_q:
        if term in result.keys():
            result[term] += 1
        else:
            result[term] = 1
    return [(key,result[key]) for key in result.keys()]
def compute_norm(vec):
    result = 0
    for key,elem in vec:
        result += elem*elem
    return math.sqrt(result)

if __name__ == "__main__":
    # dataset = load_data('mycorpus.txt')
    dataset = gutenberg.sents('milton-paradise.txt')
    edited_data = edit_data(dataset)
    # for doc in edited_data:
    # print(doc)
    dictionary = make_dict(edited_data)
    # dic = my_make_dict(edited_data)
    # corpus = my_corpus(dic, edited_data)
    # #tf_data = get_freq(corpus,edited_data)
    # idf_data = get_idf(corpus)
    # mytfidf = my_tfidf(idf_data, corpus);
    corpus = [dictionary.doc2bow(text) for text in edited_data]
    tfidf = models.TfidfModel(corpus,normalize=False)
    corpus_tfidf = tfidf[corpus] 
    index = similarities.MatrixSimilarity(corpus_tfidf)
    query = raw_input('Enter query: ')
    porter = PorterStemmer()
    query = [porter.stem(word) for word in query.lower().split()]
    new_vec = dictionary.doc2bow(query)
    sims = index[new_vec]
    sims = sorted(enumerate(sims), key=lambda item: - item[1])
    
    # my_query = proc_query(query, dic)#[(get_key(value, dic),1) for value in query]
    
    i = 0
    for key,value in sims:
        if (value == 0) or (i == 5):
            break
        for doc in dataset[key]:
            print(unicode(doc)),
        print('')
        i += 1
        
    print('End of output')
    
    # weights = get_weights(my_query, mytfidf)
    # #print(weights)
    # sorted_weights = sorted(weights, key=lambda x : x[1],reverse=True)
    # i = 0
    #
    # for key,value in sorted_weights:
    #     if (value == 0) or (i == 5):
    #         break
    #     print(str(dataset[key])+' '+str(value))
    #     i += 1
    #
    # print('End of output B')