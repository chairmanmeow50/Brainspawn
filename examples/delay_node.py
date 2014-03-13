import numpy as np
import nengo
from nengo.utils.functions import whitenoise
model = nengo.Model("Delayed connection")
input = nengo.Node(whitenoise(1, 5, seed=60))
A = nengo.Ensemble(nengo.LIF(40), dimensions=1)
nengo.Connection(input, A)

class Delay(object):
    def __init__(self, dimensions, timesteps=50):
        self.history = np.zeros((timesteps, dimensions))
    def step(self, t, x):
        self.history = np.roll(self.history, -1)
        self.history[-1] = x
        return self.history[0]

dt = 0.001
delay = Delay(1, timesteps=int(0.2 / 0.001))
delaynode = nengo.Node(delay.step, size_in=1)
nengo.Connection(A, delaynode)

B = nengo.Ensemble(nengo.LIF(40), dimensions=1)
nengo.Connection(delaynode, B)
