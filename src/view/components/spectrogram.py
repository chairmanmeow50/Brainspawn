import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np

import matplotlib.patches as mpatches
import matplotlib.lines as mlines

class Spectrogram(object):

    def __init__(self, simulator, name, func, args=(), label=None, Fs=1.0):
        self.plot_name = "spectrogram" + name
        self.simulator = simulator
        self.func = func
        self.data = self.simulator.watcher_manager.activate_watcher(name,
                func, args=args)
        self.fig = plt.figure(self.plot_name)
        self.fig.patch.set_facecolor('white')
        self.ax = plt.subplot(111)
        self.Fs = Fs # the sampling frequency
        
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.title('LFP Spectrogram')
        
        #self.draw_ui()

    def clear(self):
        # set current figure
        self.fig = plt.figure(self.plot_name)
        # clear the axes
        plt.cla() 

    def get_figure(self):
        return self.fig
    
    def get_ax(self):
        return self.ax
    
    def draw_ui(self):
        #self.ax.add_patch(mpatches.Rectangle((0,0), 5, 5))
        x,y = np.array([[-0.06, 0.0, 0.1], [0.05, -0.05, 0.05]])
        #self.ax.add_line(mlines.Line2D(x, y, 5, 1))

    def tick(self):
        # plot the output
        start = self.simulator.min_tick
        count = self.simulator.current_tick - self.simulator.min_tick
        data = self.data.get(start, count) # the signal
        data = np.reshape(data, -1)
        
        #self.clear()
        self.ax.specgram(data, Fs=self.Fs, cmap=cm.gist_heat)
        
