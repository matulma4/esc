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

def back_propagate(layers, delta):
    e = delta
    for i in range(len(layers)-1,-1,-1):
        layer = layers[i]
        layer.syn += layer.l.T.dot(e)
        layer.error = e.dot(layer.syn.T)
        layer.delta = layer.error * nonlin(layer.l,deriv=True)

        e = layer.delta


if __name__ == "__main__":
    # layer_count = 5
    # size = 4
    # layers = [NeuralLayer(size,size) for i in range(0, layer_count-2)]
    X = np.array([[0,0,1],
            [0,1,1],
            [1,0,1],
            [1,1,1]])

    y = np.array([[0],
			[1],
			[1],
			[0]])

    np.random.seed(1)

# randomly initialize our weights with mean 0
    syn0 = 2*np.random.random((3,4)) - 1
    syn1 = 2*np.random.random((4,1)) - 1


    # l_input = NeuralLayer(len(X[0]),size)
    # l_output = NeuralLayer(size,1)
    for j in xrange(100000):
        # l_input.l = nonlin(np.dot(X,l_input.syn))
        #
        # layers = propagate(layers,l_input.l)
        #
        # last = layers[layer_count-3]
        # l_output.l = nonlin(np.dot(last.l,l_output.syn))
        #
        # error = y - l_output.l # l(4,1)
        # delta = error * nonlin(l_output.l,True)
        # l_output.error = delta.dot(l_output.syn.T)
        # l_output.delta = error * nonlin(l_output.l,True)
        # l_output.syn += l_output.l.T.dot(delta)
        #
        #
        # back_propagate(layers,l_output.delta)
        #
        #
        # first = layers[0]
        # l_input.error = first.delta.dot(l_input.syn.T)
        # l_input.delta = l_input.error * nonlin(l_input.l,deriv=True)
        # first.syn += l_input.l.T.dot(first.delta)
        #
        # delta = error * nonlin(l_input.l,deriv=True)
    	# Feed forward through layers 0, 1, and 2
        l0 = X
        l1 = nonlin(np.dot(l0,syn0))
        l2 = nonlin(np.dot(l1,syn1))

        # how much did we miss the target value?
        l2_error = y - l2

        if (j% 10000) == 0:
            print "Error:" + str(np.mean(np.abs(l2_error)))

        # in what direction is the target value?
        # were we really sure? if so, don't change too much.
        l2_delta = l2_error*nonlin(l2,deriv=True)

        # how much did each l1 value contribute to the l2 error (according to the weights)?
        l1_error = l2_delta.dot(syn1.T)

        # in what direction is the target l1?
        # were we really sure? if so, don't change too much.
        l1_delta = l1_error * nonlin(l1,deriv=True)

        syn1 += l1.T.dot(l2_delta)
        syn0 += l0.T.dot(l1_delta)

    print "Output After Training:"
    print l2

