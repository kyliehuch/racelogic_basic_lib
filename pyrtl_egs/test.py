import pyrtl
import random

# functions
def min(a,b):
    return a | b

def max(a,b):
    return a & b

def inhibit(a,i):
    ''' where i inhibits a '''
    i_before_a = pyrtl.Register(bitwidth=1)
    i_before_a.next <<= i_before_a | i & ~ a
    o = a & ~ i_before_a
    return o

def delta(a,d):
    assert isinstance(d, int)
    assert (d>=0)
    if d==0:
        rval = a
    else:
        shiftreg = [pyrtl.Register(bitwidth=1) for i in range(d)]
        interwire = a
        for i in range(d):
            shiftreg[i].next <<= interwire
            interwire = shiftreg[i]
        rval = interwire
    return rval

def coinc(a,b,d):
    assert isinstance(d,int)
    assert (d>=0)
    tmp1 = min(a,b)
    tmp2 = max(a,b)
    tmp3 = delta(tmp1,d)
    out = inhibit(tmp2,tmp3)
    return out

# hardware

in1, in2 = (pyrtl.Input(1, "in" + str(x)) for x in range(1,3))
out = pyrtl.Output(1, "out")

out <<= coinc(in1,in2,3)

# simulation

in1_vals = [0,0,0,0,0,0,1,1,1,1]
in2_vals = [0,0,1,1,1,1,1,1,1,1]

sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)
for cycle in range(len(in1_vals)):
    sim.step({
        'in1': in1_vals[cycle],
        'in2': in2_vals[cycle]})

sim_trace.render_trace()
