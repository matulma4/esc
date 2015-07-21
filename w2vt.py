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
    V, N = len(vocabulary), 3
    WI = (np.random.random((V, N)) - 0.5) / N
    WO = (np.random.random((N, V)) - 0.5) / V
    input_word = raw_input("Enter query: ")
    # input_word = 'the'
    learning_rate = 1.0
    for target_word in vocabulary:
    # for input_word in vocabulary:
        for word in vocabulary:
            for j in range(2):
                p_word_given = (np.exp(-np.dot(WO.T[vocabulary[word]],
                                               WI[vocabulary[input_word]])) /
                                sum(np.exp(-np.dot(WO.T[vocabulary[w]],
                                                   WI[vocabulary[input_word]]))
                                    for w in vocabulary))
                t = 1 if word == target_word else 0
                error = t - p_word_given
                WO.T[vocabulary[word]] = (WO.T[vocabulary[word]] - learning_rate *  error * WI[vocabulary[input_word]])
                WI[vocabulary[input_word]] = WI[vocabulary[input_word]] - learning_rate * WO.sum(1)
    # query = raw_input("Enter query: ")
    #
    for word in vocabulary:
        print word,np.dot(WI[vocabulary[target_word]],
             WO.T[vocabulary[word]])
    # print WO
    # print WI



















