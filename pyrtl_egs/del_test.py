import pyrtl
import random

# --------- Function being tested ----------

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

def simple_add(k,x):
    assert isinstance(k, int)
    new_wire = x + k
    return new_wire

# --------- Hardware ----------

in1, in2 = (pyrtl.Input(8, "in" + str(x)) for x in range(1,3))
out1, out2, out3 = (pyrtl.Output(8, "out" + str(x)) for x in range(1,4))

out1 <<= in1 + in2
out2 <<= simple_add(3, in1)
out3 <<= pyrtl.probe(in1 + 3, 'adder1_probe')


# idea ? --> nope (maybe)
# out3 <<= rdelta((pyrtl.probe(in1, 'in1_probe')), in1)

# -------- Simulation ---------

# each produces list of 15 random values in the given range
vals1 = [int(2**random.uniform(1, 8) - 2) for _ in range(15)]
vals2 = [int(random.uniform(0, 36)) for _ in range(15)]

sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)
for cycle in range(len(vals1)):
    sim.step({
        'in1': vals1[cycle],
        'in2': vals2[cycle],
        })

for i in range(len(vals1)):
    assert(sim_trace.trace['out2'][i] == sim_trace.trace['out3'][i])

# the many ways to trace through values of each wire in cycles of a simulation
sim_trace.render_trace()
sim_trace.print_trace()

'''
print("out2:     ", str(sim_trace.trace['out2']))
print("out3:     ", str(sim_trace.trace['out3']))

for i in range(len(vals1)):
    print(
'''
