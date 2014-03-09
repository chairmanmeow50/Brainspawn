import matplotlib.cm as cm
from matplotlib.figure import Figure
import matplotlib.mlab as mlab
import numpy as np
from view.visualizations._visualization import Visualization

import matplotlib.patches as mpatches
import matplotlib.lines as mlines

def class_name():
    return "Spectrogram"

class Spectrogram(Visualization):

    def name(self):
        return "Spectrogram"

    def __init__(self, sim_manager, main_controller, **kwargs):
        super(Spectrogram, self).__init__(sim_manager, main_controller)
        self._figure = Figure()
        self.init_canvas(self._figure)
        self._figure.patch.set_facecolor('white')

        self.axes = self._figure.add_subplot(111)
        self.Fs = kwargs.get('Fs') if 'Fs' in kwargs else 1.0 # the sampling frequency

        self.spec_data = []

        self.axes.set_xlabel('Time (s)')
        self.axes.xaxis.set_label_coords(0.5, -0.07)
        self.axes.set_ylabel('Frequency (Hz)')
        self.axes.yaxis.set_label_coords(-0.10, 0.5)
        self.axes.set_title('LFP Spectrogram')

    @staticmethod
    def display_name(cap):
        return "Spectrogram"

    @staticmethod
    def supports_cap(cap):
        return cap.name in ['spikes']


    def clear(self):
        #plt.cla()
        pass

    def update(self, data, start_time):
        latest_i = len(data) - 1
        length = len(data[latest_i])
        sum = 0
        for i in xrange(0, length, 1):
            sum += data[latest_i][i]
        average_value = sum / length
        
        self.spec_data.append(average_value)
        
        self.clear()
        self.axes.specgram(self.spec_data, Fs=self.Fs, cmap=cm.gist_heat)

