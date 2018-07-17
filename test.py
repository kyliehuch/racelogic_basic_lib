import itertools
import pyrtl

'''
in1, in2, in3 = (pyrtl.Input(1, "in" + str(x)) for x in range(1,4))
out = pyrtl.Output(1, "out")

input = [in1,in2,in3]

out <<= pyrtl.rtl_any()

in1_vals = [0,0,1,1,1,1]
in2_vals = [0,0,0,0,1,1]
in3_vals = [0,0,0,1,1,1]

sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)
for cycle in range(len(in1_vals)):
    sim.step({
        'in1': in1_vals[cycle],
        'in2': in2_vals[cycle],
        'in3': in3_vals[cycle]})

sim_trace.render_trace()
'''

in_list = [1,1,0]

combo_list = list(itertools.combinations(in_list,2))
print(combo_list)
prod_list = [(x[0] & x[1]) for x in combo_list]
print(prod_list)

'''
def vmax(c,*args):
    wires = [("tmp" + str(x)) for x in range(len(args[0]))]
    for i in range(0,len(args[0])):
        wires[i] = args[0][i]
'''
