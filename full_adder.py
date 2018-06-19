import random
import pyrtl

# declare input and output wire vectors
a, b, c = pyrtl.Input(1, 'a'), pyrtl.Input(1, 'b'), pyrtl.Input(1, 'c')
carry_out, sum = pyrtl.Output(1, 'carry_out'), pyrtl.Output(1, 'sum')

# declare internal wire vectors
temp1, temp2 = pyrtl.WireVector(1, 'temp1'), pyrtl.WireVector(1, 'temp2')

sum <<= a ^ b ^ c

# intermediary calculations
temp1 <<= a & b
temp2 <<= b & c
temp3 = a & c # declaration and initialization of temp3, use =

carry_out <<= temp1 | temp2 | temp3

print('---------- Full Adder Implementation ----------')
print(pyrtl.working_block())
print()

print('---------- Full Adder Simulation ----------')
sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)

for cycle in range(15):
    sim.step({
        'a': random.choice([0,1]),
        'b': random.choice([0,1]),
        'c': random.choice([0,1])
        })

sim_trace.render_trace(symbol_len=5, segment_size=5)

for cycle in range(15):
    add_result = (sim_trace.trace['a'][cycle] +
                  sim_trace.trace['b'][cycle] +
                  sim_trace.trace['c'][cycle])
    python_sum = add_result & 0x1
    python_cout = (add_result >> 1) & 0x1
    if (python_sum != sim_trace.trace['sum'][cycle] or
        python_cout != sim_trace.trace['carry_out'][cycle]):
        print('This example is broken!!')
        exit(1)

exit(0)
