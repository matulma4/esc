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
    c = [WI.T[index] for index,wd in context]
    l = 1. / (1. + np.exp(-np.dot(c, w.T)))
    err = 1. - w - l
    delta = np.dot(err,w)
    WI += delta
    # WO[vocabulary[word]] += outer(err,)
    return

def docs2bow(docs, dictionary):
    """Transforms a list of strings into a list of lists where
    each unique item is converted into a unique integer."""
    for doc in docs:
        yield [dictionary[word] for word in doc.split()]

def get_context(line,size,i):
    word = line[i]
    start = max(0,i - size/2)
    end = min(len(line),start+size)
    if end == len(line):
        start = end - size
    context = line[start:i]+line[i+1:end]
    return (word,context,i)

def probability(h,target_word,WO,vocabulary):
    return (np.exp(np.dot(WO.T[vocabulary[target_word]], h)) /
                            sum(np.exp(np.dot(WO.T[vocabulary[w]], h)) for w in vocabulary))
def main():
    dataset = [line.lower() for line in open('mycorpus.txt')]
    vocabulary = Vocabulary()
    sentences_bow = list(docs2bow(dataset,vocabulary))
    learning_rate = 0.5
    V, N, P = len(vocabulary), 3, len(dataset)
    WI = (np.random.random((V, N)) - 0.5) / N
    WO = (np.random.random((N, V)) - 0.5) / V
    D =  (np.random.random((P, N)) - 0.5) / N
    # input_word = "queen"
    target_word = "dwarf"
    context = ["dwarf","hates"]
    j = 0
    for line in dataset:
        for wd in line.split():
            target_word = wd
            context = line.split()
            context.remove(wd)
            learning_rate = 0.5
            for i in range(4):
                h = np.sum([WI[vocabulary[w]] for w in context])+D[j]
                h = h/(len(context)+1)
                for word in vocabulary:

                    p = probability(h,word,WO,vocabulary)
                    t = 1 if word == target_word else 0
                    error = t - p
                    WO.T[vocabulary[word]] = (WO.T[vocabulary[word]] - learning_rate * error * h)
                for input_word in context:
                    WI[vocabulary[input_word]] = (WI[vocabulary[input_word]] - (1. / len(context)) *
                                              learning_rate * WO.sum(1))
                D[j] = D[j] - learning_rate * WO.sum(1)
                learning_rate -= 0.1
        j += 1
    print D

if __name__ == "__main__":
    # main()
    for line in open("mycorpus.txt"):
        for i in range(len(line.split())):
            print get_context(line.split(),3,i)

    # for word in vocabulary:
    #     p = probability(input_word,target_word,WI,WO,vocabulary)
    #     t = 1 if word == target_word else 0
    #     error = t - p
    #     WO.T[vocabulary[word]] = (WO.T[vocabulary[word]] - learning_rate * error * WI[vocabulary[input_word]])
    #     print word, p



















