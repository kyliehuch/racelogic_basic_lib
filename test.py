import itertools
import pyrtl

def test(*in_list):
    return pyrtl.rtl_any(*in_list)


in1, in2, in3, in4, in5 = (pyrtl.Input(1, "in" + str(x)) for x in range(1,6))
out = pyrtl.Output(1, "out")

out <<= test(in1,in2,in3,in4,in5)


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
