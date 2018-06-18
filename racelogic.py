from functools import reduce

class Infinity:
    def __repr__(self):
        return '-'
inf = Infinity() # this value will serve as our infinity


def rmin(a,b):
	''' min function '''
    if a==inf:
        return b
    elif b==inf:
        return a
    return min(a,b)

def rmax(a,b):
	''' max function '''
    if a==inf or b==inf:
        return inf
    return max(a,b)

def rd(a,c=1):
	''' delay function '''
    if a==inf or c==inf:
        return inf
    return a+c

def ri(i,x):
	''' inhibit function '''
	if i==inf:
        return x
    elif x==inf:
        return inf
    if i<=x:
        return inf
    return x

def rvd(a,b
