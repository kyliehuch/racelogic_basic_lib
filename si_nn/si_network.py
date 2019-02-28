"""
si_network.py

Very simple nn built from racelogic soft inhibit gates to classify the MNIST data - adapted from code writen by Michael Nielsen
"""

import random
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit
from math import exp

class Network(object):

    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.delays = [np.random.randn(y, 1) for y in sizes[1:]]
        self.eweights = [np.random.randn(y, x)
                        for x, y in zip(sizes[:-1], sizes[1:])]
        self.iweights = [np.random.randn(y, x)
                        for x, y in zip(sizes[:-1], sizes[1:])]


    def feedforward(self, a):
        """Return the output of the network if ``a`` is input."""
        for d, e, i in zip(self.delays, self.eweights, self.iweights):
            e_signals = np.add(a, e)
            np.append(e_signals, d)
            i_signals = np.add(a, i)
            if (min(e_signals) < min(i_signals)):
                a = min(e_signals)
                #a = sigmoid(min(e_signals))
            else:
                a = max(e_signals)
                #a = sigmoid(max(e_signals))
        return a

"""
    def SGD(self, training_data, epochs, mini_batch_size, eta,
            test_data=None):
        if test_data: n_test = len(test_data)
        n = len(training_data)
        for j in xrange(epochs):
            random.shuffle(training_data)
            mini_batches = [
                training_data[k:k+mini_batch_size]
                for k in xrange(0, n, mini_batch_size)]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta)
            if test_data:
                print "Epoch {0}: {1} / {2}".format(
                    j, self.evaluate(test_data), n_test)
            else:
                print "Epoch {0} complete".format(j)

    def update_mini_batch(self, mini_batch, eta):
        nabla_d = [np.zeros(d.shape) for d in self.delays]
        nabla_e = [np.zeros(e.shape) for e in self.eweights]
        nabla_i = [np.zeros(i.shape) for i in self.iweights]
        for x, y in mini_batch:
            delta_nabla_d, delta_nabla_e, delta_nabla_i = self.backprop(x, y)
            nabla_d = [nd+dnd for nd, dnd in zip(nabla_d, delta_nabla_d)]
            nabla_e = [ne+dne for ne, dne in zip(nabla_e, delta_nabla_e)]
            nabla_i = [ni+dni for ni, dni in zip(nabla_i, delta_nabla_i)]
        self.eweights = [e-(eta/len(mini_batch))*ne
                        for e, ne in zip(self.eweights, nabla_e)]
        self.iweights = [i-(eta/len(mini_batch))*ni
                        for i, ni in zip(self.iweights, nabla_i)]
        self.delays = [d-(eta/len(mini_batch))*nd
                       for d, nd in zip(self.delays, nabla_d)]

    def backprop(self, x, y):
        nabla_d = [np.zeros(d.shape) for d in self.delays]
        nabla_e = [np.zeros(e.shape) for e in self.eweights]
        nabla_i = [np.zeros(i.shape) for i in self.iweights]
        # feedforward
        activation = x
        activations = [x] # list to store all the activations, layer by layer
        zs = [] # list to store all the z vectors, layer by layer
        for d, e, i in zip(self.delays, self.eweights, self.iweights):
            e_signals = np.add(activation, e)
            np.append(e_signals, d)
            i_signals = np.add(activation, i)
            if (min(e_signals) < min(i_signals)):
                z = min(e_signals)
            else:
                z = max(e_signals)
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        # backward pass
        delta = self.cost_derivative(activations[-1], y) * \
            sigmoid_prime(zs[-1])



        nabla_d[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        # Note that the variable l in the loop below is used a little
        # differently to the notation in Chapter 2 of the book.  Here,
        # l = 1 means the last layer of neurons, l = 2 is the
        # second-last layer, and so on.  It's a renumbering of the
        # scheme in the book, used here to take advantage of the fact
        # that Python can use negative indices in lists.
        for l in xrange(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())
        return (nabla_b, nabla_w)

    def evaluate(self, test_data):
        test_results = [(np.argmax(self.feedforward(x)), y)
                        for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)


    def cost_derivative(self, output_activations, y):
        return (output_activations-y)

#### Miscellaneous functions
def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))

def sigmoid_prime(z):
    return sigmoid(z)*(1-sigmoid(z))

"""
