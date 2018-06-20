import random
import io
from pyrtl.rtllib import adders, multipliers
import pyrtl

random.seed(93729473)
# used to make random calls deterministic for this example

# building three inputs
in1, in2, in3 = (pyrtl.Input(8, "in" + str(x)) for x in range(1, 4))
out = pyrtl.Output(10, "out")

# adders NOT wirevectors
add1_out = adders.kogge_stone(in1, in2)
add2_out = adders.kogge_stone(add1_out, in3)
out <<= add2_out

# The most basic way of debugging PyRTL is to connect a value to an output wire
# and use the simulation to trace the output.

# Connect an output wire to the result wire of the first adder to check the result of the first addition
debug_out = pyrtl.Output(9, "debug_out")
debug_out <<= add1_out

# simulate circut
vals1 = [int(2**random.uniform(1, 8) - 2) for _ in range(20)]
vals2 = [int(2**random.uniform(1, 8) - 2) for _ in range(20)]
vals3 = [int(2**random.uniform(1, 8) - 2) for _ in range(20)]

sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)
for cycle in range(len(vals1)):
    sim.step({
        'in1': vals1[cycle],
        'in2': vals2[cycle],
        'in3': vals3[cycle]})

# to get the result data you don't need to print a waveform of the trace
# Just pull the data out of the tracer directly
print("---- Inputs and debug_out ----")
print("in1:         ", str(sim_trace.trace['in1']))
print("in2:         ", str(sim_trace.trace['in2']))
print("debug_out:   ", str(sim_trace.trace['debug_out']))

# Use the ability to directly retrieve the trace data to verify correctness of  first adder
for i in range(len(vals1)):
    assert(sim_trace.trace['debug_out'][i] == sim_trace.trace['in1'][i] + sim_trace.trace['in2'][i])


print("in3:         ", str(sim_trace.trace['in3']))
print("out:         ", str(sim_trace.trace['out']))
print('\n')

for i in range(len(vals1)):
    assert(sim_trace.trace['out'][i] == sim_trace.trace['debug_out'][i] + sim_trace.trace['in3'][i])


# --- Probe ---

# clear all hardware from current working block
pyrtl.reset_working_block()
print("---- Using Probes ----")

# In this example, we will be multiplying two numbers using tree_multiplier()
# Again, create the two inputs and an output
in1, in2 = (pyrtl.Input(8, "in" + str(x)) for x in range(1, 3))
out1, out2 = (pyrtl.Output(8, "out" + str(x)) for x in range(1, 3))

multout = multipliers.tree_multiplier(in1, in2)