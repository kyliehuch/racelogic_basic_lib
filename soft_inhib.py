# Tim Sherwood
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit
from math import exp
""" soft inhibit function tests """

NSEEDS = 100

# this is the "base unit" of the network,
# which takes two inputs, 'a' and 'b', and
# then a set of parameters.
def node(a, b, pki, pai, pbi, pae, pbe):
    i = min(a + pai, b + pbi)  # inhibit
    # if inhibit is the first to arrive
    if i <= min(a + pae, b + pbe, pki):
        # wait for all of the inputs to arrive
        return max(a + pae, b + pbe, pki)
    else:
        # fire as soon as any of the inputs arrive
        return min(a + pae, b + pbe, pki)
NPARAM = node.__code__.co_argcount - 2

# this is the network of nodes that will be trained.
# There is one hidden layer with two nodes (h0 and h1)
# and then a output node (out).  x[0] and x[1] are
# the inputs 'a' and 'b', and 'p' is the list of paramters
# which will then bee partioned up and fed to each of the
# nodes.
def ref(x,p):
    # x[0]---h0
    #     \ /  \
    #      X    out
    #     / \  /
    # x[1]---h1
    h0 = node(x[0], x[1], *pslice(p,0))
    h1 = node(x[0], x[1], *pslice(p,1))
    out = node(h0, h1, *pslice(p,2))
    return out - p[-1]
def pslice(p,set):
    return p[set*NPARAM:(set+1)*NPARAM]

# the model that defines the "right' answer.  The ref
# parameters will be trained to fit this model
def model(x):
    #return x[0] ^ x[1]  # xor
    return 0 if x[0]==1 and x[1]==1 else 1  # nand

# this function tells us how "close" a list of parameters
# p, when applied to ref above, as compared to the model.
# It is just the sum square error
def error(p):
    return sum((model(x)-ref(x,p))**2 for x in evalx)

# when training we will attempt to minimize the total "cost"
# of a set of parameters 'p'.  The biggest component of the
# cost is the error, but a small amount of addition weight
# is placed on having small constants (so that, all things
# being equal, we get more reasonable to read constants.
def cost(p):
    c = error(p) + sum([abs(x) for x in p])/1e10
    return c

# these are the 'a,b' values over which to evaluate the
# reference implementation (to see how close it fits the
# desired model).
evalx = [(0,0), (0,1), (1,0), (1,1)]

# ref_internals is just a copy of ref, but one that additionally
# returns the internal values returned by both h0 and h1.  It is
# useful mostly for debuging and understanding what is happening.
def ref_internal(x,p):
    h0 = node(x[0], x[1], *pslice(p,0))
    h1 = node(x[0], x[1], *pslice(p,1))
    out = node(h0, h1, *pslice(p,2))
    return out - p[-1], h0, h1, out

# this is the actual fitting of the parameters 'p' to the model.
# There are NPARAM parameters per node, 3 nodes, plus then one
# constant offset to renormalize the output.
total_param = 3*NPARAM+1
# each call to 'minimize' uses some fancy techniques to find the
# best set of parameters to minimize the cost, but it is very much
# subject to the initial starting point choosen.  As such, we do
# NSEEDS different mimizations in a big list, sort them, and take
# the best one.
results = [minimize(cost, x0=np.random.rand(total_param), bounds=[(0,None)]*total_param )
           for _ in range(NSEEDS)]
results.sort(key=lambda x: x.fun)
best_result = results[0]

# print out the best set of parameters
for i in range(0,total_param,NPARAM):
    print('param:', ' '.join('{0:.3f}'.format(v) for v in best_result.x[i:i+NPARAM]))

# print out the best fit found
print('ref (0,0) -> {0:0.4f}'.format(ref((0,0),(best_result.x))))
print('ref (0,1) -> {0:0.4f}'.format(ref((0,1),(best_result.x))))
print('ref (1,0) -> {0:0.4f}'.format(ref((1,0),(best_result.x))))
print('ref (1,1) -> {0:0.4f}'.format(ref((1,1),(best_result.x))))

# print out the 'right' answer for comparison
print('model (0,0) -> {0:0.4f}'.format(model((0,0))))
print('model (0,1) -> {0:0.4f}'.format(model((0,1))))
print('model (1,0) -> {0:0.4f}'.format(model((1,0))))
print('model (1,1) -> {0:0.4f}'.format(model((1,1))))

# print out some of the internal state
print('internal state (0,0) -> '+' '.join(['{0:0.4f}'.format(v) for v in ref_internal((0,0),(best_result.x))]))
print('internal state (0,1) -> '+' '.join(['{0:0.4f}'.format(v) for v in ref_internal((0,1),(best_result.x))]))
print('internal state (1,0) -> '+' '.join(['{0:0.4f}'.format(v) for v in ref_internal((1,0),(best_result.x))]))
print('internal state (1,1) -> '+' '.join(['{0:0.4f}'.format(v) for v in ref_internal((1,1),(best_result.x))]))
