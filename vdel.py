import pyrtl
import random

def rmin(a,b):
    return a | b

def rmax(a,b):
    return a & b

def rinhibit(i,a):
    ''' where i inhibits a '''
    i_before_a = pyrtl.Register(bitwidth=1)
    i_before_a.next <<= i_before_a | i & ~ a
    o = a & ~ i_before_a
    return o

def rdelta(c,x):
    assert isinstance(c, int)
    assert (c>=0)
    if c==0:
        rval = x
    else:
        shiftreg = [pyrtl.Register(bitwidth=1) for i in range(c)]
        interwire = x
        for i in range(c):
            shiftreg[i].next <<= interwire
            interwire = shiftreg[i]
        rval = interwire
    return rval

# delays signal a by time c if inhibit signal i arives before a
#   if (i<=a) return a+c , else (i>a) return a
def rVdelta(i,c,a):
    ''' variable delay function '''
    delayed_signal = rdelta(c,a)
    inhibited_signal = rinhibit(i,a)
    return rmin(delayed_signal, inhibited_signal)


# implementation of rdelta 'circut'
wire_in, delay, output = pyrtl.Input(5, 'wire_in'), pyrtl.Input(5, 'delay'), pyrtl.Output(5, 'output')

output <<= rdelta(

print('---------- rVdelta Implementation ----------')
print(pyrtl.working_block())
print()

print('---------- rVdelta Simulation ----------')
sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)

for cycle in range(15):
    sim.step({
        'inhibit': random.choice([3,4,5,6,7,8]),
        'delay': random.choice([0,1,2]),
        'wire_in': random.choice([3,4,5,6,7,8])
        })

del_value = sim_trace.trace['delay']
sim.inspect(delay)

sim_trace.render_trace(trace_list=[inhibit,wire_in,delay,output],symbol_len=5,segment_size=5)


'''
# implementation of rVdelta 'circut'
inhibit, delay, wire_in = pyrtl.Input(5, 'inhibit'), pyrtl.Input(5, 'delay'), pyrtl.Input(5, 'wire_in')
output = pyrtl.Output(5, 'output')

output <<= delay

print('---------- rVdelta Implementation ----------')
print(pyrtl.working_block())
print()

print('---------- rVdelta Simulation ----------')
sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)

for cycle in range(15):
    sim.step({
        'inhibit': random.choice([3,4,5,6,7,8]),
        'delay': random.choice([0,1,2]),
        'wire_in': random.choice([3,4,5,6,7,8])
        })

del_value = sim_trace.trace['delay']
sim.inspect(delay)

sim_trace.render_trace(trace_list=[inhibit,wire_in,delay,output],symbol_len=5,segment_size=5)
'''
