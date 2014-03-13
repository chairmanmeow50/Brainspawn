import nengo
from nengo.utils.functions import piecewise

model = nengo.Model('Controlled Integrator')

A = nengo.Ensemble(nengo.LIF(225), dimensions=2, radius=1.5)


input_func = piecewise({0: 0, 0.2: 5, 0.3: 0, 0.44: -10, 0.54: 0, 0.8: 5, 0.9: 0})

inp = nengo.Node(output=input_func)
tau = 0.1
nengo.Connection(inp, A, transform=[[tau], [0]], filter=tau)

control_func = piecewise({0: 1, 0.6: 0.5})
control = nengo.Node(output=control_func)
nengo.Connection(control, A, transform=[[0], [1]], filter=0.005)
nengo.Connection(A, A,
                 function=lambda x: x[0] * x[1],  # -- function is applied first to A\n",
                 transform=[[1], [0]],            # -- transform converts function output to new state inputs\n",
                 filter=tau)
