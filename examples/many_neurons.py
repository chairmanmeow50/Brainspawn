import nengo
model = nengo.Model('Many Neurons')
A = nengo.Ensemble(nengo.LIF(100), dimensions=1, label="A")

import numpy as np
sin = nengo.Node(output=lambda t: np.sin(8 * t))  # Input is a sine"

nengo.Connection(sin, A, filter=0.01) # 10ms filter"
