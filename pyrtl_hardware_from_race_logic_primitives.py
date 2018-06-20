import pyrtl

### Basic Race Logic Elements #########################################
#######################################################################

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

def rcoinc(a,b):
    last_a = pyrtl.Register(bitwidth=1)
    last_b = pyrtl.Register(bitwidth=1)
    holdit = pyrtl.Register(bitwidth=1)
    last_a.next <<= a
    last_b.next <<= b
    coinc_instant = a & b & (~last_a) & (~last_b)
    coinc = holdit | coinc_instant
    holdit.next <<= coinc
    return coinc

def rinput(name=None):
    return pyrtl.Input(bitwidth=1,name=name)

def routput(name=None):
    return pyrtl.Output(bitwidth=1,name=name)

### Additional Race Logic Elements ####################################
#######################################################################

# delays signal a by time c if inhibit signal i arives before a
#   if (i<=a) return a+c , else (i>a) return a
def rVdelta(i,c,a):
    ''' variable delay function '''
    delayed_signal = rdelta(c,a)
    inhibited_signal = rinhibit(i,a)
    return rmin(delayed_signal, inhibited_signal)

# returns max(a,b) if a and b arive within fixed time c of eachother
#   if (abs(a-b) < c) return rmax(a,b), else (abs(a-b) >= c) return -
def rcoinc(c,a,b):
    ''' timed max function '''
    timer = rdelta(c,rmin(a,b))
    return rinhibit(timer, rmax(a,b))

# returns max(a,b) if a and b arive within variable time c of eachother
#   delay is 'on' if i arives before the first of the two values; i <= rmin(a,b)
def rVcoinc(i,c,a,b):
    ''' variable timed max function '''
    variable_timer = rVdelta(i,c,rmin(a,b))
    return rinhibit(variable_timer, rmax(a,b))

### Functions for Testing  ############################################
#######################################################################

def race_testval(x):
    ''' generator returning race-encoded values for x '''
    if x is None:
        while True:
            yield 0
    else:
        for i in range(x):
            yield 0
        while True:
            yield 1

def decode_race(x):
    ''' given a list [0,0,...,0,1,1,...,1] decode to integer '''
    # TODO: add check that it is indeed a race logic signal
    try:
        return x.index(1)
    except ValueError:
        return None

def sim_race(input_dict):
    ''' simulates race logic design, with integer inputs and integer outputs '''
    # The inputs dict is coverted in to time-encoded inputs and fed cycle
    # by cycle to the circuit under test.  The resulting output is decoded from the
    # race encoded signal back to an integer.
    sim_trace = pyrtl.SimulationTrace()
    sim = pyrtl.Simulation(tracer=sim_trace)
    # set inputs
    simtime = max(0 if x is None else x for x in input_dict.values()) + 3
    rinput_dict = {k:race_testval(v) for k,v in input_dict.items()}
    # run simulation
    for i in range(simtime):
        sim.step({k:next(v) for k,v in rinput_dict.items()})
    # decode outputs
    output_dict = {k:decode_race(v) for k,v in sim_trace.trace.items()}
    return output_dict, sim_trace

class RaceTestError(Exception):
    pass

def r_from_str(x):
    ''' generates a named input our output from name as a string '''
    if x == 'output':
        return routput('output')
    else:
        return rinput(x)

def race_test(function):
    ''' Decorator for wrapping race-logic test functions.
        given a function with only kwargs, return a new function
        that maps each of those kwargs to a race-logic signal, runs
        the simulation, and unmaps the race-logic output back to an
        integer.  All kwargs are treated as input except for the special
        name "output" which is the signal to test at completion.'''
    def wrapper(*args, **kwargs):
        assert len(args) == 0  # only keyword args allowed
        pyrtl.reset_working_block()
        # map inputs names
        race_kwargs = {k:r_from_str(k) for k,v in kwargs.items()}
        # build the test
        function(*args, **race_kwargs)
        # run the simulation
        o,t = sim_race({race_kwargs[k]:v for k,v in kwargs.items() if k!='output'})
        # check the result of the simulation is the same as the output argument
        sim_out = o['output']
        spec_out = kwargs['output']
        if sim_out != spec_out:
            raise RaceTestError('sim output "%s" != spec output "%s"' % (sim_out, spec_out))
        pyrtl.reset_working_block()
        return t
    return wrapper

### Tests of Race Logic  ##############################################
#######################################################################

@race_test
def test_min(a, b, output):
    output <<= rmin(a, b)
test_min(a=3, b=5, output=3)
test_min(a=2, b=1, output=1)
test_min(a=3, b=None, output=3)
test_min(a=None, b=None, output=None)

@race_test
def test_max(a, b, output):
    output <<= rmax(a, b)
test_max(a=3, b=5, output=5)
test_max(a=2, b=1, output=2)
test_max(a=3, b=None, output=None)
test_max(a=None, b=0, output=None)
test_max(a=None, b=None, output=None)

@race_test
def test_inhibit(a, b, output):
    output <<= rinhibit(a, b)
test_inhibit(a=3, b=5, output=None)
test_inhibit(a=2, b=1, output=1)
test_inhibit(a=3, b=None, output=None)
test_inhibit(a=None, b=0, output=0)
test_inhibit(a=None, b=None, output=None)
