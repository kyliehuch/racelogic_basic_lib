import pyrtl
import random


# --------- Functions -----------

def rmin(a,b):
    return a | b

def rinhibit(i,a):
    ''' where i inhibits a '''
    i_before_a = pyrtl.Register(bitwidth=1)
    i_before_a.next <<= i_before_a | i & ~ a
    o = a & ~ i_before_a
    return o

def rdelta(c,x):
    assert isinstance(c, int)
    assert (c>=0)
    if c==0:
        rval = x
    else:
        shiftreg = [pyrtl.Register(bitwidth=x.bitwidth) for i in range(c)]
        interwire = x
        for i in range(c):
            shiftreg[i].next <<= interwire
            interwire = shiftreg[i]
        rval = interwire
    return rval


# ---------- Hardware -----------

input, inhibit = pyrtl.Input(1, "input"), pyrtl.Input(1, "inhibit")
output = pyrtl.Output(1, "output")
interwire1, interwire2, interwire3 = (pyrtl.WireVector(1, "interwire" + str(x)) for x in range(1,4))

# vdelta gate: if excitatory signal arrives first, passes through undelayed, if inhibitory signal arrives first exititory signal is delayed
interwire1 <<= input
interwire2 <<= rdelta(3, input)
interwire3 <<= rinhibit(inhibit, interwire1)
output <<= rmin(interwire2, interwire3)

# ---------- Simulation ----------

'''
# undelayed signal - excitory signal arrives first
in_vals = [0,0,1,1,1,1,1,1,1,1]
inhib_vals = [0,0,0,0,1,1,1,1,1,1]
'''


# delayed signal - inhibitory signal arives first
in_vals = [0,0,1,1,1,1,1,1,1,1]
inhib_vals = [0,1,1,1,1,1,1,1,1,1]


sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)
for cycle in range(len(in_vals)):
    sim.step({
        'input': in_vals[cycle],
        'inhibit': inhib_vals[cycle]})

sim_trace.render_trace(trace_list=[input,inhibit,output])
