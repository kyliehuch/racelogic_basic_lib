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

# takes list of wirevectors and number of signals required to 'fire' (refered to
# fire as "threshold") as inputs
def rvmax(t,*in_list):
    combo_list = list(itertools.combinations(in_list,t))
    prod_list = [pyrtl.rtl_all(*x) for x in combo_list]
    o = pyrtl.rtl_any(*prod_list)
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


# --------- Hardware -------------

in1, in2, in3, in4, in5 = (pyrtl.Input(1, "in" + str(x)) for x in range(1,6))
out = pyrtl.Output(1, "out")

# fire if the first 4 edges arive within 2 cycles of each other
out <<= rvcoinc(4,2,in1,in2,in3,in4,in5)


# --------- Simulation ------------

in1_vals = [0,0,1,1,1,1,1,1]
in2_vals = [0,0,0,0,1,1,1,1]
in3_vals = [0,0,0,1,1,1,1,1]
in4_vals = [0,0,0,0,0,0,1,1]
in5_vals = [0,0,0,0,0,1,1,1]

sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)
for cycle in range(len(in1_vals)):
    sim.step({
        'in1': in1_vals[cycle],
        'in2': in2_vals[cycle],
        'in3': in3_vals[cycle],
        'in4': in4_vals[cycle],
        'in5': in5_vals[cycle]})

sim_trace.render_trace()
