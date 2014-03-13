import nengo
from nengo.objects import Uniform
model = nengo.Model('Two Neurons')
neurons = nengo.Ensemble(nengo.LIF(2),
                         dimensions=1,  # Representing a scalar\n",
                         intercepts=Uniform(-.5, -.5),  # Set the intercepts at .5\n",
                         max_rates=Uniform(100,100),  # Set the max firing rate at 100hz\n",
                         encoders=[[1],[-1]])  # One 'on' and one 'off' neuron"
import numpy as np
sin = nengo.Node(output=lambda t: np.sin(8 * t))
nengo.Connection(sin, neurons, filter=0.01)
