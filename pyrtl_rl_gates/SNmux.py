import pyrtl

# -------- Primatives ----------

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

#----------- SN ------------

# hardcoded for 4 inputs
def sn(a,b,c,d):
    imin1 = rmin(a,b)
    imax1 = rmax(a,b)
    imin2 = rmin(c,d)
    imax2 = rmax(c,d)
    o1 = rmin(imin1,imin2)
    i2 = rmax(imin1,imin2)
    i3 = rmin(imax1,imax2)
    o4 = rmax(imax1,imax2)
    o2 = rmin(i2,i3)
    o3 = rmax(i2,i3)
    return (o1,o2,o3,o4)

#---------- Hardware ---------

in1, in2, in3, in4 = (pyrtl.Input(1, "in" + str(x)) for x in range(1,5))
o1, o2, o3, o4 = (pyrtl.WireVector(1, "o" + str(x)) for x in range(1,5))
out = pyrtl.Output(1, "out")
temp1, temp2, temp3 = (pyrtl.WireVector(1, "temp" + str(x)) for x in range(1,4))
n, m = pyrtl.Const(1,2), pyrtl.Const(2,2)


outs = sn(in1,in2,in3,in4)
o1 <<= outs[0]
o2 <<= outs[1]
o3 <<= outs[2]
o4 <<= outs[3]

temp1 <<= pyrtl.mux(n,o1,o2,o3,o4)
temp2 <<= rdelta(2,temp1)
temp3 <<= pyrtl.mux(m,o1,o2,o3,o4)
out <<= rinhibit(temp2,temp3)

#--------- Simulation ---------

in1_vals = [0,0,1,1,1,1,1,1]
in2_vals = [0,0,0,0,0,1,1,1]
in3_vals = [0,1,1,1,1,1,1,1]
in4_vals = [0,0,0,0,0,0,1,1]

sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)
for cycle in range(len(in1_vals)):
    sim.step({
        'in1': in1_vals[cycle],
        'in2': in2_vals[cycle],
        'in3': in3_vals[cycle],
        'in4': in4_vals[cycle]})

sim_trace.render_trace()
