import nengo
model = nengo.Model('Controlled Integrator 2')
A = nengo.Ensemble(nengo.LIF(225), dimensions=2, radius=1.5)

from nengo.utils.functions import piecewise
input_func = piecewise({0.2: 5, 0.3: 0, 0.44: -10, 0.54: 0, 0.8: 5, 0.9: 0})
inp = nengo.Node(output=input_func)
tau = 0.1
nengo.Connection(inp, A, transform=[[tau], [0]], filter=0.1)

control_func = piecewise({0: 0, 0.6: -0.5})
control = nengo.Node(output=control_func)
nengo.Connection(control, A, transform=[[0], [1]], filter=0.005)

nengo.Connection(A, A,
                 function=lambda x: x[0] * x[1] + x[0],
                 transform=[[1], [0]],
                 filter=tau)

