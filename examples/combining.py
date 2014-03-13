import nengo
import numpy as np

model = nengo.Model('Combining')

A = nengo.Ensemble(nengo.LIF(100), dimensions=1)
B = nengo.Ensemble(nengo.LIF(100), dimensions=1)

output = nengo.Ensemble(nengo.LIF(200), dimensions=2, label='2D Population')

sin = nengo.Node(output=np.sin)
cos = nengo.Node(output=np.cos)

nengo.Connection(sin, A)
nengo.Connection(cos, B)

nengo.Connection(A, output, transform=[[1], [0]])
nengo.Connection(B, output, transform=[[0], [1]])
