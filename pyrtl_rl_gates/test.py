import pyrtl

# -------- Functions ----------

def rmin(a,b):
    return a | b

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

def race(a, pae, pke):
    return rmin(rdelta(pke, k), rdelta(pae, a))

# -------- Hardware ----------

in1, k = pyrtl.Input(1, "in1"), pyrtl.Input(1, "k")
out = pyrtl.Output(1, "out")
out <<= race(in1, 2, 3)

in1_vals = [1,1,1,1,1,1,1]
k_vals = [1,1,1,1,1,1,1]

sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)
for cycle in range(len(in1_vals)):
    sim.step({
            'in1': in1_vals[cycle],
            'k': k_vals[cycle]})

sim_trace.render_trace()
