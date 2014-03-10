import matplotlib.cm as cm
import numpy as np
from view.visualizations._visualization import Visualization, registered_plot

import matplotlib.patches as mpatches
import matplotlib.lines as mlines

@registered_plot
class Spectrogram(Visualization):

    def __init__(self, main_controller, obj, cap):
        super(Spectrogram, self).__init__(main_controller, obj, cap)

        self.axes.set_xlabel('Time (s)')
        self.axes.xaxis.set_label_coords(0.5, -0.07)
        self.axes.set_ylabel('Frequency (Hz)')
        self.axes.yaxis.set_label_coords(-0.10, 0.5)

    @staticmethod
    def plot_name():
        return "Spectrogram"

    @staticmethod
    def supports_cap(cap):
        return cap.name in ['spikes']

    def update(self, start_step, step_size, data):
        # TODO - start_step
        self.axes.clear()
        if len(data) > 2:
            self.axes.specgram(np.average(data, 1), Fs=1/step_size, cmap=cm.gist_heat)

