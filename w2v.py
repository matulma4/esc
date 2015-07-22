import numpy as np
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

if __name__ == "__main__":
    l_rate = 5
    dataset = set("In 1943 President Roosevelt and British Prime Minister Winston Churchill opened a wartime conference in Casablanca".lower().split())
    length = len(dataset)
    dic = make_dict(dataset,length)
    onehot = []
    for key in dic.keys():
        tmp = [0 for s in range(0,length)]
        tmp[key] = 1
        onehot.append(tmp)
    x = np.array(onehot)
    #print(x)
    np.random.seed(1)
    Wa = 2*np.random.random((1,length)) - 1 # 1x15
    Wb = 2*np.random.random((length,5)) - 1 # 15x14
    for i in range(0, len(x)-1):
        # print x[i].T
        x_input = np.array([x[i]]).T #15x1
        out_start = i - 2
        if out_start < 0:
            out_start = 0
        out_end = out_start + 5
        if out_end > len(x) - 1:
            out_end  = len(x) - 1
            out_start = out_end - 5
        y_output = np.concatenate((x[out_start:i],x[i+1:out_end + 1]),axis=0).T # 15x14
        # print(y_output)
        # print(x_input)
        for j in xrange(10000):
            l0 = x_input #15x1
            l1 = nonlin(np.dot(l0,Wa)) # 15x15
            l2 = nonlin(np.dot(l1,Wb)) # 15x14

            l2_error = y_output - l2

            if j == 9999:
                print "Error:" + str(np.mean(np.abs(l2_error)))

            l2_delta = l2_error*nonlin(l2,deriv=True) * l_rate# 15x14

            l1_error = l2_delta.dot(Wb.T) # 15x14 *

            l1_delta = l1_error * nonlin(l1,deriv=True) * l_rate

            Wb += l1.T.dot(l2_delta)
            Wa += l0.T.dot(l1_delta)
    # print Wa
    # print Wb
    query = np.zeros(shape=(1,len(dic)))
    query[0][5] = 1
    a = nonlin(np.dot(nonlin(np.dot(query.T,Wa)),Wb))
    j = 0
    b = []
    for term in a:
        b.append((j,a[j]))
        j += 1
    b = sorted(b,key=lambda x : x[1],reverse=True)
    for key,value in b:
        print dic[key],value