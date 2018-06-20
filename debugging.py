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

# The following line will create a probe named 'std_probe" for later use, like an output.
pyrtl.probe(multout, 'std_probe')

# The probe returns multout, the original wire, and multout * 2 will be assigned to out1
out1 <<= pyrtl.probe(multout, 'stdout_probe') * 2

# probe can also be used with other operations like this:
pyrtl.probe(multout + 32, 'adder_probe')

# or this:
pyrtl.probe(multout[2:7], 'select_probe')

# or, similarly:
# (this will create a probe of multout while passing multout[2:16] to out2)
out2 <<= pyrtl.probe(multout)[2:16]

# probe can be used on any wire any time, even before or during its operation, assignment, etc.

# Now on to the simulation...
# For variation, we'll recreate the random inputs:
vals1 = [int(2**random.uniform(1, 8) - 2) for _ in range(10)]
vals2 = [int(2**random.uniform(1, 8) - 2) for _ in range(10)]

sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)
for cycle in range(len(vals1)):
    sim.step({
        'in1': vals1[cycle],
        'in2': vals2[cycle]})

# Now we will show the values of the inputs and probes
# and look at that, we didn't need to make any outputs!
# (although we did, to demonstrate the power and convenience of probes)
sim_trace.render_trace()
sim_trace.print_trace()

print("--- Probe w/ debugging: ---")
# Say we wanted to have gotten more information about
# one of those probes above at declaration.
# We could have used pyrtl.set_debug_mode() before their creation, like so:
pyrtl.set_debug_mode()
pyrtl.probe(multout - 16, 'debugsubtr_probe')
pyrtl.set_debug_mode(debug=False)


# ---- WireVector Stack Trace ----
# WireVector Stack Traces allow you to find out more about where a particular
# WireVector was made in your code. With this enabled the WireVector will
# store exactly were it was created, which should help with issues where
# there is a problem with an identified wire.

# Like above, just add the following line before the relevant WireVector
# might be made or at the beginning of the program.
pyrtl.set_debug_mode()

print("---- Stack Trace ----")
test_out = pyrtl.Output(9, "test_out")
test_out <<= adders.kogge_stone(in1, in2)

# Now to retreive information
wire_trace = test_out.init_call_stack

# This data is generated using the traceback.format_stack() call from the Python standard library's Traceback module (look at the Python standard library docs for details on the function). Therefore, the stack traces are stored as a list with the outermost call first.

for frame in wire_trace:
    print(frame)

# Storage of Additional Debug Data

# ------------------------------------
# WARNING: the debug information generated by the following two processes are
# not guaranteed to be preserved when functions (eg. pyrtl.synthesize() ) are
# done over the block.
# ------------------------------------

# However, if the stack trace does not give you enough information about the
# WireVector, you can also embed additional information into the wire itself
# Two ways of doing so is either through manipulating the name of the
# WireVector, or by adding your own custom metadata to the WireVector

# So far, each input and output WireVector have been given their own names, but
# normal WireVectors can also be given names by supplying the name argument to
# the constructor

dummy_wv = pyrtl.WireVector(1, name="blah")

# Also, because of the flexible nature of Python, you can also add custom
# properties to the WireVector.

dummy_wv.my_custom_property_name = "John Clow is great"
dummy_wv.custom_value_028493 = 13

# removing the WireVector from the block to prevent problems with the rest of
# this example
pyrtl.working_block().remove_wirevector(dummy_wv)

# ---- Trivial Graph Format ----

# Finally, there is a handy way to view your hardware creations as a graph.
# The function output_to_trivialgraph will render your hardware a formal that
# you can then open with the free software "yEd"
# (http://en.wikipedia.org/wiki/YEd). There are options under the
# "hierarchical" rendering to draw something that looks quite like a circuit.

pyrtl.working_block().sanity_check()
pyrtl.passes._remove_unused_wires(pyrtl.working_block()) # so that trivial_graph() will work

print("--- Trivial Graph Format  ---")
with io.StringIO() as tgf:
    pyrtl.output_to_trivialgraph(tgf)
    print(tgf.getvalue())
