import nengo
tau = 0.1
model = nengo.Model('Integrator')
integrator = nengo.networks.Integrator(tau, neurons=nengo.LIF(100), dimensions=1)
from nengo.utils.functions import piecewise
input = nengo.Node(piecewise({0: 0, 0.2: 1, 1: 0, 2: -2, 3: 0, 4: 1, 5: 0}))
nengo.Connection(input, integrator.input, filter=tau)
