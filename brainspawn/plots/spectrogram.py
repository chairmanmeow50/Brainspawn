from plots.base_plot import registered_plot
from plots.plot import Plot
import matplotlib.cm as cm
import numpy as np

@registered_plot
class Spectrogram(Plot):

    def __init__(self, main_controller, obj, cap):
        super(Spectrogram, self).__init__(main_controller, obj, cap)

        self.axes = self.figure.add_subplot(111)
        self.axes.patch.set_alpha(0.0)
        self.axes.set_title(self.title)
        self.axes.set_ylabel("Frequency (Hz)")
        self.axes.set_xlabel("Time (s)")
        self.axes.set_xlim([0, 1])
        self._image = None

    @staticmethod
    def plot_name():
        return "Spectrogram"

    @staticmethod
    def supports_cap(cap):
        return cap.name in ["spikes"]

    def update(self, start_step, step_size, data):
        if self._image:
            self._image.remove()
            self._image = None
        if len(data) <= 2:
            return
        start_time = start_step * step_size
        end_time = (start_step + data.shape[0]) * step_size
        Pxx, freqs, bins, self._image = self.axes.specgram(
                np.average(data, 1), Fs=1.0/step_size, cmap=cm.gist_heat, xextent=(start_time, end_time))
        self.axes.set_xlim([start_time, max(end_time, 1)])
