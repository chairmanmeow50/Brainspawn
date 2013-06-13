from spa_sequence.spa_sequence import net, pThal

import matplotlib.animation as animation
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import time

class Spectrogram(object):
    def __init__(self):
        # this initial tick takes a long time (~2 seconds)
        net.run(0.001)

        self.fig = plt.figure()
        ax1 = plt.subplot(211)
        self.line, = ax1.plot([], [])
        self.ax2 = plt.subplot(212, sharex=ax1)
        self.Fs = 1.0 / pThal.dt_sample  # the sampling frequency

    def start_animate(self):
        # set the animation interval based on the time to animate one step
        t0 = time.time()
        self.animate(0)
        interval = max(0, 30 - 1000 * (time.time() - t0))
        self._ani = animation.FuncAnimation(self.fig, self.animate, interval=interval, blit=True)

    def animate(self, i):
        # run the simulator for another step
        net.run(0.005)

        # plot the output
        x = pThal.get_data()[:,0]  # the signal
        t = np.linspace(0.0, net.run_time, x.size)
        self.line.set_data(t, x)
        Pxx, freqs, bins, im = self.ax2.specgram(x, Fs=self.Fs, cmap=cm.gist_heat)
        return self.line, im

if __name__ == "__main__":
    spec = Spectrogram()
    spec.start_animate()
    plt.show()
