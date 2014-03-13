import nengo

model = nengo.Model('Integrator')
A = nengo.Ensemble(nengo.LIF(100), dimensions=1, label='Integrator')

from nengo.utils.functions import piecewise
input = nengo.Node(piecewise({0: 0, 0.2: 1, 1: 0, 2: -2, 3: 0, 4: 1, 5: 0}), label='Piecewise input')

tau = 0.1
nengo.Connection(A, A, transform=[[1]], filter=tau) # Using a long time constant for stability\n"
nengo.Connection(input, A, transform=[[tau]], filter=tau) # The same time constant as recurrent to make it more 'ideal'"
