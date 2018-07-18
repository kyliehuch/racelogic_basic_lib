import pyrtl
import itertools

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

# vdelta gate: if excitatory signal arrives first, passes through undelayed, if inhibitory signal arrives first exititory signal is delayed
#interwire1 <<= input
def vrdelta(c,i,x):
    interwire1 = rdelta(c, x)
    interwire2 = rinhibit(i, x)
    o = rmin(interwire1, interwire2)
    return o

# takes list of wirevectors and number of signals required to 'fire' (refered to
# fire as "threshold") as inputs
def rvmax(t,*in_list):
    combo_list = list(itertools.combinations(in_list,t))
    prod_list = [pyrtl.rtl_all(*x) for x in combo_list]
    o = pyrtl.rtl_any(*prod_list)
    return o

# modified max gate that allows signal through if input signals arive within delay time and block signals otherwise (signals allowed through if they arive on delay time)
def rcoinc(c,x,y):
    timer_start = rmin(x, y)
    timer = rdelta(c, timer_start)
    interwire = rmax(x, y)
    o = rinhibit(timer, interwire)
    return o

# modified max gate that allows signal through if the threshold number of
# input signals arive within delay time and block signals otherwise (signals
# allowed through if they arive on delay time)
def rvcoinc(theshold, sensitivity_window, *in_list):
    timer_start = pyrtl.rtl_any(*in_list)
    timer = rdelta(sensitivity_window, timer_start)
    interwire = rvmax(theshold, *in_list)
    o = rinhibit(timer, interwire)
    return o


# --------- Skeleton Neuron -----------

# exct_inputs and inhib_inputs are both lists of wirevectors
def neuron(delay, threshold, sens_window, exct_inputs, inhib_inputs):
    inhibit = pyrtl.rtl_any(*inhib_inputs)
    interwire = rvcoinc(threshold, sens_window, *exct_inputs)
    signal = rdelta(delay, interwire)
    o = rinhibit(inhibit, signal)
    return o

# ------------ Hardware --------------

ex1, ex2, ex3, ex4, ex5 = (pyrtl.Input(1, "ex" + str(x)) for x in range(1,6))
inhb1, inhb2, inhb3 = (pyrtl.Input(1, "inhb" + str(x)) for x in range(1,4))
out = pyrtl.Output(1, "out")

ex_list = [ex1, ex2, ex3, ex4, ex5]
inhb_list = [inhb1, inhb2, inhb3]

out <<= neuron(0,3,2,ex_list,inhb_list)


# --------- Simulation ------------

ex1_vals = [0,0,1,1,1,1,1,1]
ex2_vals = [0,0,0,0,1,1,1,1]
ex3_vals = [0,0,0,1,1,1,1,1]
ex4_vals = [0,0,0,0,0,0,1,1]
ex5_vals = [0,0,0,0,0,1,1,1]

inhb1_vals = [0,0,0,0,0,0,0,0]
inhb2_vals = [0,0,0,1,1,1,1,1]
inhb3_vals = [0,0,0,0,0,0,0,0]

sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)
for cycle in range(len(ex1_vals)):
    sim.step({
        'ex1': ex1_vals[cycle],
        'ex2': ex2_vals[cycle],
        'ex3': ex3_vals[cycle],
        'ex4': ex4_vals[cycle],
        'ex5': ex5_vals[cycle],
        'inhb1': inhb1_vals[cycle],
        'inhb2': inhb2_vals[cycle],
        'inhb3': inhb3_vals[cycle]})

sim_trace.render_trace()
