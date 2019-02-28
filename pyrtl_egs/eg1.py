import pyrtl
import random

#-------- Hardware ----------

temp1 = pyrtl.WireVector(bitwidth=1, name='temp1')
temp2 = pyrtl.WireVector(bitwidth=1, name='temp2')

a, b, c = pyrtl.Input(1, 'a'), pyrtl.Input(1, 'b'), pyrtl.Input(1, 'c')
sum, carry_out = pyrtl.Output(1, 'out'), pyrtl.Output(1, 'carry_out')

#-------- Logic -----------

sum <<= a ^ b ^ c
temp1 <<= a & b
temp2 <<= b & c
temp3 = a & c
carry_out <<= temp1 | temp2 | temp3

print('--- One Bit Adder Implementation ---')
print(pyrtl.working_block())
print()

#------- Simulation ---------

sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)

for cycle in range(15):
    sim.step({
        'a': random.choice([0,1]),
        'b': random.choice([0,1]),
        'c': random.choice([0,1])
        })

print('--- One Bit Adder Simulation ---')
sim_trace.render_trace(symbol_len=5, segment_size=5)

a_value = sim.inspect(a)
print("The last value of a was: " + str(a_value))
