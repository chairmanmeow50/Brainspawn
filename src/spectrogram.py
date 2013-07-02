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
        self.ax1 = plt.subplot(211)
        self.line, = self.ax1.plot([], [])
        self.ax2 = plt.subplot(212, sharex=self.ax1)
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
        # 0 refers to the 0th signal, there are 5 signals actually
        
        x = pThal.get_data()[:,0]
        print x
        #xcropped=x[x.size-100:x.size,0]  # the signal
        t = np.linspace(0, net.run_time, x.size)
        print t
        if (x.size > 100):
            print "x.size:" + str(x.size)
            x = x[x.size-100:x.size-1]
            t = t[t.size-100:t.size-1]
        self.line, = self.ax1.plot(t, x)
        self.ax1.set_xlim(t[0], t[t.size-1])
        self.line.set_data(t, x)
        
        Pxx, freqs, bins, im = self.ax2.specgram(x, Fs=self.Fs, cmap=cm.gist_heat)
        return self.line, im

def main():
    spec = Spectrogram()
    spec.start_animate()
    #while (True): 
    #    net.run(0.005)
    
    plt.show()
        
if __name__ == "__main__":
    main()
