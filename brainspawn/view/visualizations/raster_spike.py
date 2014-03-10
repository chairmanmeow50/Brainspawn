import numpy as np
from matplotlib import rcParams
from view.visualizations._visualization import Visualization
import __future__

def class_name():
    return "Raster_Spike_Plot"

class Raster_Spike_Plot(Visualization):

    @staticmethod
    def plot_name():
        return "Raster Spike Plot"

    @staticmethod
    def supports_cap(cap):
        return cap.name in ['spikes']

    def update(self, start_step, step_size, spikes):
        trange = np.linspace(start_time, end_time, spikes.shape[0])

        color_cycle = rcParams['axes.color_cycle']
        colors = [color_cycle[ix % len(color_cycle)]
                       for ix in range(spikes.shape[1])]

        spikes = [trange[spikes[:, i] > 0].flatten()
                  for i in range(spikes.shape[1])]
        for ix in range(len(spikes)):
            if spikes[ix].shape == (0,):
                spikes[ix] = np.array([-1])
        self.axes.eventplot(spikes, colors=colors)
        self.axes.set_ylim(len(spikes) - 0.5, -0.5)
        if len(spikes) == 1:
            self.axes.set_ylim(0.4, 1.6)  # eventplot plots different for len==1
        self.axes.set_xlim(left=0)

    def __init__(self, main_controller, obj, cap):
        super(Raster_Spike_Plot, self).__init__(main_controller, obj, cap)

        self.axes.set_xlim([0, 1])
        self.axes.set_ylim([0, 1])

