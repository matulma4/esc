import numpy as np

alphas = [0.001,0.01,0.1,1,10,100,1000]
alpha = 10
# compute sigmoid nonlinearity
def sigmoid(x):
    output = 1/(1+np.exp(-x))
    return output

# convert output of sigmoid function to its derivative
def sigmoid_output_to_derivative(output):
    return output*(1-output)
if __name__ == "__main__":
    Xs = []
    Xs.append(np.array([[1,0,0],
                [0,0,0],
                [0,0,1]]))
    Xs.append(np.array([[0,0,0],
                [0,1,0],
                [0,0,1]]))
    Xs.append(np.array([[1,0,0],
                [0,1,0],
                [0,0,0]]))
    ys = []
    ys.append(np.array([[0],
                [1],
                [0]]))
    ys.append(np.array([[1],
                [0],
                [0]]))
    ys.append(np.array([[0],
                [0],
                [1]]))
    hidden_layer = 4
    # for alpha in alphas:
      #  print "\nTraining With Alpha:" + str(alpha)
    np.random.seed(1)

    # randomly initialize our weights with mean 0
    synapse_0 = 2*np.random.random((len(Xs[0][0]),hidden_layer)) - 1
    synapse_1 = 2*np.random.random((hidden_layer,len(ys[0][0]))) - 1
    for i in range(3):
        X = Xs[i]
        y = ys[i]
        for j in xrange(60000):

            # Feed forward through layers 0, 1, and 2
            layer_0 = X
            layer_1 = sigmoid(np.dot(layer_0,synapse_0))
            layer_2 = sigmoid(np.dot(layer_1,synapse_1))

            # how much did we miss the target value?
            layer_2_error = layer_2 - y

            if (j% 10000) == 0:
                print "Error after "+str(j)+" iterations:" + str(np.mean(np.abs(layer_2_error)))

            # in what direction is the target value?
            # were we really sure? if so, don't change too much.
            layer_2_delta = layer_2_error*sigmoid_output_to_derivative(layer_2)

            # how much did each l1 value contribute to the l2 error (according to the weights)?
            layer_1_error = layer_2_delta.dot(synapse_1.T)

            # in what direction is the target l1?
            # were we really sure? if so, don't change too much.
            layer_1_delta = layer_1_error * sigmoid_output_to_derivative(layer_1)

            synapse_1 -= alpha * (layer_1.T.dot(layer_2_delta))
            synapse_0 -= alpha * (layer_0.T.dot(layer_1_delta))
        print(synapse_0)

        print sigmoid(np.dot(sigmoid(np.dot(X,synapse_0)),synapse_1))
        # print("Output after training:")


