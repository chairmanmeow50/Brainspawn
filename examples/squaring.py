import nengo
model = nengo.Model('Squaring')
A = nengo.Ensemble(nengo.LIF(100), dimensions=1)
B = nengo.Ensemble(nengo.LIF(100), dimensions=1)

import numpy as np
sin = nengo.Node(output=np.sin)
nengo.Connection(sin, A)
def square(x):
    return x[0] * x[0]
nengo.Connection(A, B, function=square)
