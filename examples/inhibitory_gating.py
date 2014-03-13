import nengo

model = nengo.Model("Inhibitory Gating")
n_neurons = 30
A = nengo.Ensemble(nengo.LIF(n_neurons), dimensions=1)
B = nengo.Ensemble(nengo.LIF(n_neurons), dimensions=1)
C = nengo.Ensemble(nengo.LIF(n_neurons), dimensions=1)

import numpy as np
from nengo.utils.functions import piecewise

sin = nengo.Node(output=np.sin)
inhib = nengo.Node(output=piecewise({0: 0, 2.5: 1, 5: 0, 7.5: 1, 10: 0, 12.5: 1}))

nengo.Connection(sin, A)
nengo.Connection(sin, B)
nengo.Connection(inhib, A.neurons, transform=[[-2.5]] * n_neurons)
nengo.Connection(inhib, C)
nengo.Connection(C, B.neurons, transform=[[-2.5]] * n_neurons)
