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

    def get_figure(self):
        return self.fig

    def tick(self):
        # plot the output
        start = self.simulator.min_tick
        count = self.simulator.current_tick - self.simulator.min_tick
        data = self.data.get(start, count) # the signal
        t = np.linspace(start, start +
                data.size * self.simulator.dt, data.size)
        #print "min: " + str(self.simulator.min_tick) + ", max: " + str(data.size * self.simulator.dt) + ", size: " + str(data.size)

        tsize = t.size
        if (tsize > 200):
            t = t[tsize-200:tsize]
            data = data[tsize-200:tsize]

        self.line.set_data(t, data)
        Pxx, freqs, bins, im = self.ax2.specgram(data, Fs=self.Fs,
                cmap=cm.gist_heat)
        return self.line, im
