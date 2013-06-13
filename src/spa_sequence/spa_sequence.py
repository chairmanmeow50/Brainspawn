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

class Spectrogram():
    def __init__(self):
        
        self.net = nef.Network('Sequence', seed=1)
        seq = Sequence(self.net)

        self.pThal = self.net.make_probe('thal.rule', dt_sample=0.001)
        # pGPi = net.make_probe('BG.GPi', dt_sample=0.001, data_type='spikes')
        # pState = net.make_probe('state.buffer', dt_sample=0.001, data_type='spikes')

        # this initial tick takes a long time (~2 seconds)
        self.net.run(0.001)
        # net.write_data_to_hdf5('sequence.hd5')

        self.fig = plt.figure()
        ax1 = plt.subplot(211)
        self.line, = ax1.plot([], [])
        self.ax2 = plt.subplot(212, sharex=ax1)
        self.Fs = 1.0 / self.pThal.dt_sample  # the sampling frequency

        # set the animation interval based on the time to animate one step
    def start_animate(self, animate_fig, animate_func):
        self.t0 = time.time()
        self.animate(0)
        interval = max(0, 30 - 1000 * (time.time() - self.t0))
        return animation.FuncAnimation(animate_fig, animate_func, interval=interval, blit=True)
        #plt.show()

    def get_interval(self):
        return max(0, 30 - 1000 * (time.time() - self.t0))

    def get_figure(self):
        return self.fig

    def animate(self, i):
        print "ANIMATING!!"
    # run the simulator for another step
        self.net.run(0.005)

    # plot the output
        x = self.pThal.get_data()[:,0]  # the signal
        t = np.linspace(0.0, self.net.run_time, x.size)
        self.line.set_data(t, x)
        Pxx, freqs, bins, im = self.ax2.specgram(x, Fs=self.Fs, cmap=cm.gist_heat)
        return self.line, im


#spec = Spectrogram()
#figure = spec.get_figure()
#ani = spec.start_animate(figure, spec.animate)
#plt.show()

