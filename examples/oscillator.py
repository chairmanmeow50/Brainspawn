import nengo
model = nengo.Model('Oscillator')
neurons = nengo.Ensemble(nengo.LIF(200), dimensions=2)

from nengo.utils.functions import piecewise
input = nengo.Node(output=piecewise({0: [1, 0], 0.1: [0, 0]}))
nengo.Connection(input, neurons)
nengo.Connection(neurons, neurons, transform=[[1, 1], [-1, 1]], filter=0.1)
