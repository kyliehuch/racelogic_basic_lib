import pyrtl
import itertools


in1, in2, in3 = (pyrtl.Input(1, "in" + str(x)) for x in range(1,4))
in_list = [in1, in2, in3]
#interwire1, interwire2 = pyrtl.WireVector(1, "interwire1"), pyrtl.WireVector(1, "interwire2")
out = pyrtl.Output(1, "out")

combo_list = list(itertools.combinations(in_list,2))
prod_list = [(x[0] & x[1]) for x in combo_list]

'''
interwire2 <<= prod_list.pop()

while prod_list:
    interwire1 <<= (interwire2 | prod_list.pop())
    interwire2 <<= interwire1

out <<= interwire2
'''

'''
# hardcoded solution (works)
out <<= (combo_list[0][0] & combo_list[0][1]) | (combo_list[1][0] & combo_list[1][1]) | (combo_list[2][0] & combo_list[2][1])
'''

out <<= pyrtl.rtl_any(*prod_list)


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
