import spa
import nengo_theano as nef

import matplotlib.animation as animation
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import time

class Rules:
    def A(state='A'):
        effect(state='B')
    def B(state='B'):
        effect(state='C')
    def C(state='C'):
        effect(state='D')
    def D(state='D'):
        effect(state='E')
    def E(state='E'):
        effect(state='A')

class Sequence(spa.SPA):
    dimensions = 8
    verbose = True

    state = spa.Buffer()
    BG = spa.BasalGanglia(Rules)
    thal = spa.Thalamus(BG)

    input = spa.Input(0.1, state='D')

net = nef.Network('Sequence', seed=1)
seq = Sequence(net)

pThal = net.make_probe('thal.rule', dt_sample=0.001)
# pGPi = net.make_probe('BG.GPi', dt_sample=0.001, data_type='spikes')
# pState = net.make_probe('state.buffer', dt_sample=0.001, data_type='spikes')

# this initial tick takes a long time (~2 seconds)
net.run(0.001)
# net.write_data_to_hdf5('sequence.hd5')

fig = plt.figure()
ax1 = plt.subplot(211)
line, = ax1.plot([], [])
ax2 = plt.subplot(212, sharex=ax1)
Fs = 1.0 / pThal.dt_sample  # the sampling frequency

def animate(i):
    # run the simulator for another step
    net.run(0.005)

    # plot the output
    x = pThal.get_data()[:,0]  # the signal
    t = np.linspace(0.0, net.run_time, x.size)
    line.set_data(t, x)
    Pxx, freqs, bins, im = ax2.specgram(x, Fs=Fs, cmap=cm.gist_heat)
    return line, im

# set the animation interval based on the time to animate one step
t0 = time.time()
animate(0)
interval = max(0, 30 - 1000 * (time.time() - t0))
ani = animation.FuncAnimation(fig, animate, interval=interval, blit=True)
plt.show()
