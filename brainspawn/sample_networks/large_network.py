"""Test representation of large network
"""

import nengo
import numpy as np

num_ensembles = 20

model = nengo.Model("large network")
neurons = []
for i in range(num_ensembles):
    neurons.append(nengo.Ensemble(nengo.LIF(100), dimensions=2))

    sin = nengo.Node(output=np.sin)
    cos = nengo.Node(output=np.cos)

    nengo.Connection(sin, neurons[i], transform=[[1], [0]])
    nengo.Connection(cos, neurons[i], transform=[[0], [1]])

    if i >= 1:
        nengo.Connection(cos, neurons[i-1], transform=[[0], [1]])
    if i >= 2 and i % 2 == 0:
        nengo.Connection(sin, neurons[i-2], transform=[[0], [1]])

