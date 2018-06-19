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

# delays signal a by time c if inhibit signal i arives before a
#   if (i<=a) return a+c , else (i>a) return a
def rvd(a,c,i):
    ''' variable delay function '''
    delayed_signal = rd(a,c)
    inhibited_signal = ri(i,a)
    return rmin(delayed_signal, inhibited_signal)

# returns max(a,b) if a and b arive within fixed time c of eachother
#   if (abs(a-b) < c) return rmax(a,b), else (abs(a-b) >= c) return -
def rcoincidence(a,b,c):
    ''' timed max function '''
    timer = rd(rmin(a,b),c)
    return ri(timer, rmax(a,b))

# returns max(a,b) if a and b arive within variable time c of eachother
#   delay is 'on' if i arives before the first of the two values; i <= rmin(a,b)
def rvcoincidence(a,b,c,i):
    ''' variable timed max function '''
    variable_timer = rvd(rmin(a,b),c,i)
    return ri(variable_timer, rmax(a,b))

# tests:
print("rmin(inf,5) = ", rmin(inf,5))
print("rd(5,2) = ", rd(5,2))
print("ri(5,2) = ", ri(5,2))
print("ri(2,5) = ", ri(2,5))
print("rvd(5,2,8) = ", rvd(5,2,8))
print("rvd(5,2,3) = ", rvd(5,2,3))
print("rvd(5,2,7) = ", rvd(5,2,7))
print("rvd(5,2,6) = ", rvd(5,2,6))
print("rvd(5,2,5) = ", rvd(5,2,5))
print("rcoincidence(5,2,1) = ", rcoincidence(5,2,1))
print("rcoincidence(5,2,4) = ", rcoincidence(5,2,4))
print("rcoincidence(5,2,3) = ", rcoincidence(5,2,3))
print("rcoincidence(5,2,3.1) = ", rcoincidence(5,2,3.1))
print("rvcoincidence(5,2,4,3) = ", rvcoincidence(5,2,4,3)) # delay off
print("rvcoincidence(5,2,4,1) = ", rvcoincidence(5,2,4,1)) # delay on
print("rvcoincidence(5,2,1,3) = ", rvcoincidence(5,2,1,3)) # delay off
print("rvcoincidence(5,2,1,1) = ", rvcoincidence(5,2,1,1)) # delay on
