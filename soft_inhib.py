# Tim Sherwood
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit
""" soft inhibit function tests """

"""
def node(a, b, dai, dbi, dki, dae, dbe, dke):
    i = min(a+dai, b+dbi, dki)
    if i <= min(a+dae, b+dbe, dke):
        return max(a+dae, b+dbe, dke)
    else:
        return min(a+dae, b+dbe, dke)
NPARAM = 6
"""

#def node(a, b, pai, pbi, pki, pae, pbe):
#    i = min(a + pai, b + pbi, pki)
#    if i <= min(a + pae, b + pbe):
#        return min(a + pae, b + pbe)
#    else:
#        return max(a + pae, b + pbe)
#NPARAM = node.__code__.co_argcount - 2

def node(a, b, pki, pai, pbi, pae, pbe):
    i = min(a + pai, b + pbi, pki)
    if i <= min(a + pbe, b + pbe):
        return min(a + pae, b + pbe)
    else:
        return max(a + pae, b + pbe)
NPARAM = node.__code__.co_argcount - 2


evalx = [(0,0), (0,1), (1,0), (1,1)]
def cost(p):
    c = error(p) + sum([abs(x) for x in p])/1e10
    return c
def error(p):
    return sum((model(x)-ref(x,p))**2 for x in evalx)
def model(x):
    #return expit(0.7*x[0] + -0.2*x[1])  # nn
    return x[0] ^ x[1]  # xor
    #return 0 if x[0]==1 and x[1]==1 else 1  # nand
def pslice(p,set):
    return p[set*NPARAM:(set+1)*NPARAM]
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
def ref_internal(x,p):
    h0 = node(x[0], x[1], *pslice(p,0))
    h1 = node(x[0], x[1], *pslice(p,1))
    out = node(h0, h1, *pslice(p,2))
    return out - p[-1], h0, h1, out


total_param = 3*NPARAM+1
results = [minimize(cost, x0=np.random.rand(total_param), bounds=[(0,None)]*total_param )
           for _ in range(100)]
results.sort(key=lambda x: x.fun)

best_result = results[0]
for i in range(0,total_param,NPARAM):
    print('param:', ' '.join('{0:.3f}'.format(v) for v in best_result.x[i:i+NPARAM]))

#print('{0:0.4f}'.format(ref((0,0),(best_result.x))))
#print('{0:0.4f}'.format(ref((0,1),(best_result.x))))
#print('{0:0.4f}'.format(ref((1,0),(best_result.x))))
#print('{0:0.4f}'.format(ref((1,1),(best_result.x))))

print('model (0,0) -> {0:0.4f}'.format(model((0,0))))
print('model (0,1) -> {0:0.4f}'.format(model((0,1))))
print('model (1,0) -> {0:0.4f}'.format(model((1,0))))
print('model (1,1) -> {0:0.4f}'.format(model((1,1))))

print(' '.join(['{0:0.4f}'.format(v) for v in ref_internal((0,0),(best_result.x))]))
print(' '.join(['{0:0.4f}'.format(v) for v in ref_internal((0,1),(best_result.x))]))
print(' '.join(['{0:0.4f}'.format(v) for v in ref_internal((1,0),(best_result.x))]))
print(' '.join(['{0:0.4f}'.format(v) for v in ref_internal((1,1),(best_result.x))]))
