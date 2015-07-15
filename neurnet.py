import numpy as np


class NeuralLayer:
    def __init__(self,rows,columns):
        self.syn = 2*np.random.random((rows,columns)) - 1
        self.l = []
        self.error = []
        self.delta = []



# sigmoid function
def nonlin(x,deriv=False):
    if(deriv==True):
        return x*(1-x)
    return 1/(1+np.exp(-x))



def propagate(layers,X):
    l = X
    for layer in layers:
        layer.l = nonlin(np.dot(l,layer.syn))
        l = layer.l

    return layers

def back_propagate(layers, y, synapse):
    e = y
    s = synapse
    for i in range(len(layers)-1,-1,-1):
        layer = layers[i]
        layer.error = e.dot(s.T)
        layer.delta = layer.error * nonlin(layer.l,deriv=True)
        s += layer.l.T.dot(e)
        e = layer.delta
        s = layer.syn


if __name__ == "__main__":
    layer_count = 5
    size = 8
    layers = [NeuralLayer(size,size) for i in range(0, layer_count-2)]
    # input dataset
    X = np.array([  [0,0,1],
                    [0,1,1],
                    [1,0,1],
                    [1,1,1] ])

    # output dataset
    y = np.array([[0,1,1,0]]).T

    # seed random numbers to make calculation
    # deterministic (just a good practice)
    np.random.seed(1)


    l_input = NeuralLayer(len(X[0]),size)
    l_output = NeuralLayer(size,1)
    for j in xrange(50000):
        l_input.l = nonlin(np.dot(X,l_input.syn))

        new_l = propagate(layers,l_input.l)

        last = layers[layer_count-3]
        l_output.l = nonlin(np.dot(last.l,l_output.syn))
        error = y - l_output.l
        # print(error)
        delta = error * nonlin(l_output.l,True)
        # print(delta)

        back_propagate(layers,delta,l_output.syn)
        l_output.syn += l_output.l.T.dot(delta)

        first = layers[0]
        l_input.error = first.delta.dot(first.syn.T)
        l_input.delta = l_input.error * nonlin(l_input.l,deriv=True)
        first.syn += l_input.l.T.dot(first.delta)
        # error = l_input.delta.dot(l_input.syn.T)

        # delta = error * nonlin(l_input.l,deriv=True)
        # forward propagation
        # l0 = X
        # l1 = nonlin(np.dot(l0,syn0))
        # l2 = nonlin(np.dot(l1,syn1))
        #
        # # how much did we miss?
        # l2_error = y - l2
        #
        #
        # # multiply how much we missed by the
        # # slope of the sigmoid at the values in l1
        # l2_delta = l2_error * nonlin(l2,True)
        # if (j % 10000 == 0):
        #     print l2_delta
        #     print syn1.T
        # # update weights
        # l1_error = l2_delta.dot(syn1.T)
        # l1_delta = l1_error * nonlin(l1,deriv=True)
        # syn1 += l1.T.dot(l2_delta)
        # syn0 += l0.T.dot(l1_delta)

    print "Output After Training:"
    # print l_output.l
    print l_output.l

