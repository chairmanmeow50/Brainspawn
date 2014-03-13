import nengo
tau = 0.1   # Post-synaptic time constant for feedback\n",
w_max = 10  # Maximum frequency is w_max/(2*pi)\n",
model = nengo.Model('Controlled Oscillator')
oscillator = nengo.Ensemble(nengo.LIF(500), dimensions=3, radius=1.7)

def feedback(x):
    x0, x1, w = x  # These are the three variables stored in the ensemble\n",
    return x0 + w*w_max*tau*x1, x1 - w*w_max*tau*x0, 0

nengo.Connection(oscillator, oscillator, function=feedback, filter=tau)
frequency = nengo.Ensemble(nengo.LIF(100), dimensions=1)
nengo.Connection(frequency, oscillator, transform=[[0], [0], [1]])

from nengo.utils.functions import piecewise

initial = nengo.Node(piecewise({0: [1, 0, 0], 0.15: [0, 0, 0]}))
nengo.Connection(initial, oscillator)
input_frequency = nengo.Node(piecewise({0: 1, 1: 0.5, 2: 0, 3: -0.5, 4: -1}))
nengo.Connection(input_frequency, frequency)
