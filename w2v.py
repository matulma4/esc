import numpy as np
from collections import defaultdict
def make_dict(dataset,length):
    result = {}
    i = 0
    for doc in dataset:
        if not doc in result.values():
            result[i] = doc
        i += 1
    return result

def nonlin(x,deriv=False):
    if(deriv==True):
        return x*(1-x)
    return 1/(1+np.exp(-x))


def Vocabulary():
    dictionary = defaultdict()
    dictionary.default_factory = lambda: len(dictionary) - 1
    return dictionary

def train_sentence(sentence,WI,WO,vocabulary):
    sent = list(enumerate(sentence.split()))
    for index,word in sent:
        start = max(0,index - 2)
        end = min(len(sentence),start + 5)
        context = [sent[i] for i in range(start,end) if i != index]
        train_pair(word,context,WI,WO,vocabulary)
    return

def train_pair(word,context,WI,WO,vocabulary):
    w = WO[vocabulary[word]]
    c = [WI[index] for index,wd in context]
    l = 1. / (1. + np.exp(-np.dot(c, w.T)))
    err = 1. - w - l
    delta = np.dot(err,w)
    WI += delta
    WO[vocabulary[word]] += outer(err,)
    return
def docs2bow(docs, dictionary):
    """Transforms a list of strings into a list of lists where
    each unique item is converted into a unique integer."""
    for doc in docs:
        yield [dictionary[word] for word in doc.split()]


if __name__ == "__main__":
    dataset = [line.lower() for line in open('mycorpus.txt')]
    vocabulary = Vocabulary()
    sentences_bow = list(docs2bow(dataset,vocabulary))
    np.random.seed(11)
    dimension = 5
    window = 5
    WI = 2*np.random.random((window,dimension)) - 1
    WO = 2*np.random.random((dimension,len(vocabulary))) - 1
    for sentence in dataset:
        train_sentence(sentence,WI,WO,vocabulary)



















