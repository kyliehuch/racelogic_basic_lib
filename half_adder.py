import random
import pyrtl

# memory block object is implicity declared

# Two special types of WireVectors are Input and Output, which are used to specify an interface to the hardware block.
a, b = pyrtl.Input(1, 'a'), pyrtl.Input(1, 'b')
carry_out, sum = pyrtl.Output(1, 'carry_out'), pyrtl.Output(1, 'sum')

# calculations
sum <<= a ^ b # connect the result of a & b to the pre-allocated wirevector
carry_out <<= a & b    # <<= means 'sto'

# print working block
# You can access the working block through pyrt.working_block()
print('----------- Half Adder Implementation -----------')
print(pyrtl.working_block())
print()

# Simulate disign
# make simulation trace, make simulation that uses that trace
sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)

# call "sim.step" to simulate each clock cycle of the design
for cycle in range(15):
    sim.step({
        'a': random.choice([0, 1]),
        'b': random.choice([0, 1])
        })

# print the trace results to the screen using "render_trace"
print('----------- Half Adder Simulation -----------')
sim_trace.render_trace(symbol_len=5, segment_size=5)

a_value = sim.inspect(a)
print("The last value of a was: " + str(a_value))

# check the trace to make sure that sum and carry_out are actually
# the right values when compared to a python's addition operation
# Note that we are doing all arithmetic on values NOT wirevectors here
for cycle in range(15):
    add_result = (sim_trace.trace['a'][cycle] +
                  sim_trace.trace['b'][cycle])
    python_sum = add_result & 0x1
    python_cout = (add_result >> 1) & 0x1
    if (python_sum != sim_trace.trace['sum'][cycle] or
        python_cout != sim_trace.trace['carry_out'][cycle]):
        print('This example is broken!')
        exit(1)

exit(0)
