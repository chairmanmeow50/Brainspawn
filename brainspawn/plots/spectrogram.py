import matplotlib.cm as cm
import numpy as np
from plots.plot import Plot
from plots.base_plot import registered_plot

import matplotlib.patches as mpatches
import matplotlib.lines as mlines

@registered_plot
class Spectrogram(Plot):

    def __init__(self, main_controller, obj, cap):
        super(Spectrogram, self).__init__(main_controller, obj, cap)

        self.axes = self.figure.add_subplot(111) # take first from list
        self.axes.patch.set_alpha(0.0)
        self.axes.set_title(self.title)
        self.axes.set_xlabel('Time (s)')
        self.axes.set_ylabel('Frequency (Hz)')

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

