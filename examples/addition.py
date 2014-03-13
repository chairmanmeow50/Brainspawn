import nengo
model = nengo.Model('Addition')

A = nengo.Ensemble(nengo.LIF(100), dimensions=1)
B = nengo.Ensemble(nengo.LIF(100), dimensions=1)
C = nengo.Ensemble(nengo.LIF(100), dimensions=1)

input_a = nengo.Node(output=0.5)
input_b = nengo.Node(output=0.3)

nengo.Connection(input_a, A)
nengo.Connection(input_b, B)

nengo.Connection(A, C)
nengo.Connection(B, C)
