import pyrtl
import random

random.seed(93729473) # used to make random calls deterministic

def rdelta(c,x):
    assert isinstance(c, int)
    assert (c>=0)
    if c==0:
        rval = x
    else:
        shiftreg = [pyrtl.Register(bitwidth=1) for i in range(c)]
        interwire = x
        for i in range(c):
            shiftreg[i].next <<= interwire
            interwire = shiftreg[i]
        rval = interwire
    return rval

def bridge(a,x):
    c = a.bitmask
    return rdelta(c,x)

input, delay, output = pyrtl.Input(8, 'input'), pyrtl.Input(8, 'delay'), pyrtl.Output(8, 'output')

in_vals = [int(random.uniform(1, 8)) for _ in range(15)]
del_vals = [int(random.uniform(0, 4)) for _ in range(15)]

output <<= bridge(delay, input)

sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)
for cycle in range(len(in_vals)):
    sim.step({
        'input': in_vals[cycle],
        'delay': del_vals[cycle]})


print("input:   ", str(sim_trace.trace['input']))
print("delay:   ", str(sim_trace.trace['delay']))
print("output

sim_trace.render_trace()

''''
def bridge(a,x):
    c =

input = pyrtl.Input(8, 'input')
delay = pyrtl.Input(8, 'delay')
temp = pyrtl.WireVector(8, 'temp')
output = pyrtl.Output(8, 'output')

temp <<
output <<= rdelta(  , input)

in_vals = [int(2**random.uniform(1, 8) - 2) for _ in range(15)]

sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)
for cycle in range(len(vals))):
    sim.step({
        'input': random.uniform(1, 8),
'''
