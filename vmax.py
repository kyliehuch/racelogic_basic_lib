import pyrtl
import itertools

# --------- Function ------------

# takes list of wirevectors and number of signals required to 'fire' (refered to
# fire as "threshold") as inputs
def vmax(t,*in_list):
    combo_list = list(itertools.combinations(in_list,t))
    prod_list = [pyrtl.rtl_all(*x) for x in combo_list]
    o = pyrtl.rtl_any(*prod_list)
    return o


# --------- Hardware -------------

in1, in2, in3, in4, in5 = (pyrtl.Input(1, "in" + str(x)) for x in range(1,6))
out = pyrtl.Output(1, "out")

out <<= vmax(5,in1,in2,in3,in4,in5)


# --------- Hardcoded Solution ---------

'''
in_list = [in1, in2, in3]
combo_list = list(itertools.combinations(in_list,2))
prod_list = [(x[0] & x[1]) for x in combo_list]

out <<= pyrtl.rtl_any(*prod_list)
'''


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
