"""Basic 2d representation example
"""

import nengo
import numpy as np

# 100 LIF neurons
model = nengo.Model("2d Rep")
neurons = nengo.Ensemble(nengo.LIF(100), dimensions=2)

sin = nengo.Node(output=np.sin)
cos = nengo.Node(output=np.cos)

nengo.Connection(sin, neurons, transform=[[1], [0]])
nengo.Connection(cos, neurons, transform=[[0], [1]])

