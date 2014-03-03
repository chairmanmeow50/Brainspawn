import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
from view.visualizations.__visualization import Visualization

import matplotlib.patches as mpatches
import matplotlib.lines as mlines

def class_name():
    return "Spectrogram"

class Spectrogram(Visualization):

    def name(self):
        return "Spectrogram"

    def __init__(self, sim_manager, main_controller, **kwargs):
        super(Spectrogram, self).__init__(sim_manager, main_controller)
        self._figure = plt.figure()
        self.init_canvas(self._figure)
        self._figure.patch.set_facecolor('white')

        #self.simulator = simulator
        #self.func = func
        #self.data = self.simulator.watcher_manager.activate_watcher(name,
        #        func, args=args)
        #self.fig = plt.figure(self.plot_name)
        #self.fig.patch.set_facecolor('white')
        self.ax = plt.subplot(111)
        self.Fs = kwargs.get('Fs') if 'Fs' in kwargs else 1.0 # the sampling frequency

        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.title('LFP Spectrogram')

        #self.draw_ui()

    @staticmethod
    def display_name(cap):
        return "Spectrogram"

    @staticmethod
    def supports_cap(cap, dimensions):
        return cap.name in ['spikes']


    def clear(self):
        # set current figure
        #self.fig = plt.figure(self.plot_name)
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

    def update(self, data, start_time):
        # plot the output
        buffer_start = start_time/self.sim_manager.dt
        count = self.sim_manager.current_step - buffer_start
        '''
        start = self.simulator.min_tick
        count = self.simulator.current_tick - self.simulator.min_tick
        data = self.data.get(start, count) # the signal
        data = np.reshape(data, -1)
        '''
        self.clear()
        self.ax.specgram(data, Fs=self.Fs, cmap=cm.gist_heat)

