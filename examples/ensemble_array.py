import nengo
import numpy as np

model = nengo.Model('Ensemble Array')

sin = nengo.Node(output=lambda t: [np.cos(t), np.sin(t)])

A = nengo.networks.EnsembleArray(nengo.LIF(100), 2)
B = nengo.Ensemble(nengo.LIF(100), 2)
C = nengo.networks.EnsembleArray(nengo.LIF(100), 2)

nengo.Connection(sin, A.input)
nengo.Connection(A.output, B)
nengo.Connection(B, C.input)
