import pyrtl

'''
def vmax(c,*args):
    wires = [("tmp" + str(x)) for x in range(len(args[0]))]
    for i in range(0,len(args[0])):
        wires[i] = args[0][i]
'''

in1, in2, in3 = (pyrtl.Input(1, "in" + str(x)) for x in range(1,4))
out = pyrtl.Output(1, "out")

# wait for any 2 signals - hardcoded
out <<= (in1 & in2) | (in2 & in3) | (in1 & in3)

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
