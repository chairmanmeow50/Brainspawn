import nengo

model = nengo.Model('Lorenz attractor')
state = nengo.Ensemble(nengo.LIF(2000), 3, radius=60)

tau = 0.1
sigma = 10
beta = 8.0/3
rho = 28

def feedback(x):
    dx0 = -sigma * x[0] + sigma * x[1]
    dx1 = -x[0] * x[2] - x[1]
    dx2 = x[0] * x[1] - beta * (x[2] + rho) - rho
    return [dx0 * tau + x[0],
            dx1 * tau + x[1], 
            dx2 * tau + x[2]]

nengo.Connection(state, state, function=feedback, filter=tau)
