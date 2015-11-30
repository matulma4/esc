import pickle
from doc_to_vec import Questions
from gensim import models
import numpy as np

def count_inversion(lst):
    return merge_count_inversion(lst)[1]

def merge_count_inversion(lst):
    if len(lst) <= 1:
        return lst, 0
    middle = int( len(lst) / 2 )
    left, a = merge_count_inversion(lst[:middle])
    right, b = merge_count_inversion(lst[middle:])
    result, c = merge_count_split_inversion(left, right)
    return result, (a + b + c)

def merge_count_split_inversion(left, right):
    result = []
    count = 0
    i, j = 0, 0
    left_len = len(left)
    while i < left_len and j < len(right):
        if left[i] >= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            count += left_len - i
            j += 1
    result += left[i:]
    result += right[j:]
    return result, count

if __name__ == "__main__":
    # print count_inversion([1,2,3,4,5])
    (w,theta) = pickle.load(open("regress.pickle"))
    classes = {}
    j = 0
    for t in theta:
        classes[t] = j
        j += 1
    model = models.Doc2Vec.load("model.doc2vec")
    for docvec in model.docvecs:
        k = np.dot(docvec,w)
        i = [t for t in theta if k > t]
        print classes[min(i)]