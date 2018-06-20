import pyrtl

token_in = pyrtl.Input(1, 'token_in')
req_refund = pyrtl.Input(1, 'req_refund')
dispense = pyrtl.Output(1, 'dispense')
refund = pyrtl.Output(1, 'refund')
state = pyrtl.Register(3, 'state')

WAIT, TOK1, TOK2, TOK3, DISPENSE, REFUND = [pyrtl.Const(x, bitwidth=3) for x in range(6)]

with pyrtl.conditional_assignment:
    with req_refund: # signal of highest precedence
        state.next |= REFUND
    with token_in: # if token received, advance state in counter sequence
        with state == WAIT:
            state.next |= TOK1
        with state == TOK1:
            state.next |= TOK2
        with state == TOK2:
            state.next |= TOK3
        with state == TOK3:
            state.next |= DISPENSE # 4th token recived, dispense
        with pyrtl.otherwise:
            state.next |= REFUND
            # token received but in state where we can't handle it
    with (state == DISPENSE) | (state == REFUND):
        state.next |= WAIT
        # NOTE: the parens are needed because in Python the "|" operator is lower precedence
        # than the "==" operator!

dispense <<= state == DISPENSE
refund <<= state == REFUND

sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)

sim_inputs = {
    'token_in':   '0010100111010000',
    'req_refund': '1100010000000000'
    }

for cycle in range(len(sim_inputs['token_in'])):
    sim.step({w: int(v[cycle]) for w, v in sim_inputs.items()})

sim_trace.render_trace(trace_list=['token_in', 'req_refund', 'state', 'dispense', 'refund'])
