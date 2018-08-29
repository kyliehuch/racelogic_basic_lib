import pyrtl

# -------- Functions ----------

def rmin(a,b):
    return a | b

def rmax(a,b):
    return a & b

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
        shiftreg = [pyrtl.Register(bitwidth=1) for i in range(c)]
        interwire = x
        for i in range(c):
            shiftreg[i].next <<= interwire
            interwire = shiftreg[i]
        rval = interwire
    return rval

# modified max gate that allows signal through if input signals arive within delay time and block signals otherwise (signals allowed through if they arive on delay time)
def rcoincidence(c,x,y):
    timer_start = rmin(x, y)
    timer = rdelta(c, timer_start)
    interwire = rmax(x, y)
    o = rinhibit(timer, interwire)
    return o

# ---------- Hardware ----------

in1, in2 = pyrtl.Input(1, "in1"), pyrtl.Input(1, "in2")
output = pyrtl.Output(1, "output")

'''
# ---------- Hardcoded Function ----------

timer_start = rmin(in1, in2)
timer = rdelta(3, timer_start)
interwire = rmax(in1, in2)
output <<= rinhibit(timer, interwire)
'''

output <<= rcoincidence(3, in1, in2)


# ---------- Simulation ----------

'''
# signals arive within delay time - gate allows signal through
in1_vals = [0,0,1,1,1,1,1,1,1,1]
in2_vals = [0,0,0,1,1,1,1,1,1,1]

# signals arive at delay time - gate allows signal through
in1_vals = [0,0,1,1,1,1,1,1,1,1]
in2_vals = [0,0,0,0,0,1,1,1,1,1]
'''

# signals arive outside delay time - gate blocks signal
in1_vals = [0,0,1,1,1,1,1,1,1,1]
in2_vals = [0,0,0,0,0,0,0,1,1,1]



sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)
for cycle in range(len(in1_vals)):
    sim.step({
        'in1': in1_vals[cycle],
        'in2': in2_vals[cycle]})

sim_trace.render_trace(trace_list=[in1,in2,output])
