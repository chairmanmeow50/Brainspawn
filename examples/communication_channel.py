import numpy as np
import nengo

model = nengo.Model("Communications Channel")

sin = nengo.Node(output=np.sin)

A = nengo.Ensemble(nengo.LIF(100), dimensions=1)
B = nengo.Ensemble(nengo.LIF(100), dimensions=1)

nengo.Connection(sin, A)
nengo.Connection(A, B)
