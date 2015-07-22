import numpy as np
from collections import defaultdict

def Vocabulary():
    dictionary = defaultdict()
    dictionary.default_factory = lambda: len(dictionary)
    return dictionary

def docs2bow(docs, dictionary):
    """Transforms a list of strings into a list of lists where
    each unique item is converted into a unique integer."""
    for doc in docs:
        yield [dictionary[word] for word in doc.split()]


if __name__ == "__main__":
    sentences = [
    'the king loves the queen',
    'the queen loves the king',
    'the dwarf hates the king',
    'the queen hates the dwarf',
    'the dwarf poisons the king',
    'the dwarf poisons the queen']
    vocabulary = Vocabulary()
    sentences_bow = list(docs2bow(sentences,vocabulary))
    V, N = len(vocabulary), 10
    WI = (np.random.random((V, N)) - 0.5) / N
    WO = (np.random.random((N, V)) - 0.5) / V
    # target_word = ("king")
    # context = ['queen', 'loves']
    learning_rate = 1.0
    # for target_word in vocabulary:
    # for input_word in vocabulary:
    # h = (WI[vocabulary['queen']] + WI[vocabulary['loves']]) / 2
    sents = [sentence.split() for sentence in sentences]
    for sentence in sents:
        for i in range(0,len(sentence)):
            target_word = sentence[i]
            if i == 0:
                context = sentence[i+1:]
            else:
                context = np.concatenate((sentence[:i],sentence[i+1:]),axis=0)

            for j in range(20):
                h = 0
                for cw in context:
                    h += WI[vocabulary[cw]]
                h /= len(context)
                for word in vocabulary:
                    p = (np.exp(-np.dot(WO.T[vocabulary[word]], h)) /
                        sum(np.exp(-np.dot(WO.T[vocabulary[w]], h))
                            for w in vocabulary))
                    print word,p
                    if p == np.nan:
                        p = 0
                    t = 1 if word == target_word else 0
                    error = t - p
                    WO.T[vocabulary[word]] = (WO.T[vocabulary[word]] - learning_rate * error * h)
                for word in context:
                    WI[vocabulary[word]] = (WI[vocabulary[word]] - (1. / len(context)) * learning_rate * WO.sum(1))
    query = raw_input("Enter query: ").split()
    #
    h = 0
    for cw in query:
        h += WI[vocabulary[cw]]
    h /= len(query)
    for word in vocabulary:
         p = (np.exp(-np.dot(WO.T[vocabulary[word]],
                                           h)) /
                            sum(np.exp(-np.dot(WO.T[vocabulary[w]],
                                               h)) for w in vocabulary))
         print word,p
    # print WO
    # print WI



















