import numpy as np
def make_dict(dataset,length):
    result = {}
    i = 0
    for doc in dataset:
        result[i] = doc
        i += 1
    return result

if __name__ == "__main__":
    dataset = set("In 1943 President Roosevelt and British Prime Minister Winston Churchill opened a wartime conference in Casablanca".lower().split())
    length = len(dataset)
    dic = make_dict(dataset,length)
    onehot = []
    for key in dic.keys():
        tmp = [0 for s in range(0,length)]
        tmp[key] = 1
        onehot.append(tmp)
    x = np.matrix(onehot)
    print(x)
    W = np.zeros(shape=(length,length))
    h =