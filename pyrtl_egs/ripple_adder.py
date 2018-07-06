import pyrtl

# full adder
def one_bit_add(a, b, carry_in):
    assert len(a) == len(b) == 1
    sum = a ^ b ^ carry_in
    carry_out = (a & b) | (a & carry_in) | (b & carry_in)
    return sum, carry_out

# N-bit ripple carry adder using full adder
def ripple_add(a, b, carry_in=0):
    a, b = pyrtl.match_bitwidth(a, b)
    # function that allows us to match the bitwidth of multiple different wires
    # By default, it zero extends the shorter bits
    if len(a) == 1:
        sumbits, carry_out = one_bit_add(a, b, carry_in)
    else:
        lsbit, ripplecarry = one_bit_add(a[0], b[0], carry_in)
        msbits, carry_out = ripple_add(a[1:], b[1:], ripplecarry)
        sumbits = pyrtl.concat(msbits, lsbit)
    return sumbits, carry_out

# 3-bit adder
counter = pyrtl.Register(bitwidth=3, name='counter')
sum, carry_out = ripple_add(counter, pyrtl.Const("1'b1"))
counter.next <<= sum
# const is type of basic WireVector: holds constant values
# Registers are just like wires, except their updates are delayed to the next
# clock cycle
# This is made explicit in the syntax through the property '.next'
# which should always be set for registers.

sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)
for cycle in range(15):
    sim.step({})
    assert sim.value[counter] == cycle % 8
sim_trace.render_trace()

exit(0)
