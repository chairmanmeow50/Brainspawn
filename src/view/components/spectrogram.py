import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np


class Spectrogram(object):

    def __init__(self, simulator, name, func, args=(), label=None, Fs=1.0):
        self.simulator = simulator
        self.func = func
        self.data = self.simulator.watcher_manager.activate_watcher(name,
                func, args=args)
        self.fig = plt.figure()
        ax1 = plt.subplot(211)
        self.line, = ax1.plot([], [])
        self.ax2 = plt.subplot(212, sharex=ax1)
        self.Fs = Fs # the sampling frequency

    def tick(self):
        # plot the output
        data = self.data.get(self.simulator.min_tick) # the signal
        t = np.linspace(self.simulator.min_tick, self.simulator.min_tick +
                data.size * self.simulator.dt, data.size)
        self.line.set_data(t, data)
        Pxx, freqs, bins, im = self.ax2.specgram(data, Fs=self.Fs,
                cmap=cm.gist_heat)
        return self.line, im
