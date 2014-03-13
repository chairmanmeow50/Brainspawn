import nengo
from nengo.objects import Uniform
model = nengo.Model('A Single Neuron')
neuron = nengo.Ensemble(nengo.LIF(1),
                        dimensions=1, # Represent a scalar\n",
                        intercepts=Uniform(-.5, -.5),  # Set intercept to 0.5\n",
                        max_rates=Uniform(100, 100),  # Set the maximum firing rate of the neuron to 100hz\n",
                        encoders=[[1]])  # Sets the neurons firing rate to increase for positive input"

import numpy as np
cos = nengo.Node(lambda t: np.cos(8 * t))
nengo.Connection(cos, neuron)
