import numpy as np
from matplotlib.figure import Figure
from matplotlib import rcParams
from view.visualizations._visualization import Visualization
import __future__

def class_name():
    return "Raster_Spike_Plot"

class Raster_Spike_Plot(Visualization):
    def out_cap(self):
        return "spikes"

    @staticmethod
    def display_name(cap):
        return "Raster Spike Plot"

    @staticmethod
    def supports_cap(cap):
        return cap.name in ['spikes']

    def clear(self):
        pass

    def update(self, data, start_time):
        time = self.sim_manager.sim.trange()
        spikes = data[:len(data)-2]

        color_cycle = rcParams['axes.color_cycle']
        colors = [color_cycle[ix % len(color_cycle)]
                       for ix in range(spikes.shape[1])]

        #print time
        #print spikes
        spikes = [time[spikes[:, i] > 0].flatten()
                  for i in range(spikes.shape[1])]
        for ix in range(len(spikes)):
            if spikes[ix].shape == (0,):
                spikes[ix] = np.array([-1])
        self.axes.eventplot(spikes, colors=colors)
        self.axes.set_ylim(len(spikes) - 0.5, -0.5)
        if len(spikes) == 1:
            self.axes.set_ylim(0.4, 1.6)  # eventplot plots different for len==1
        self.axes.set_xlim(left=0)

        '''if (len(time) > 0):
            for i in range(spikes.shape[1]):
                self.ax.plot(time[spikes[:, i] > 0],
                             np.ones_like(np.where(spikes[:, i] > 0)).T + i, ',',
                             color=colors[i])'''

    def __init__(self, sim_manager, main_controller, **kwargs):
        super(Raster_Spike_Plot, self).__init__(sim_manager, main_controller)

        self._figure = Figure()

        self.init_canvas(self._figure)
        self._figure.patch.set_facecolor('white')

        self.axes = self._figure.add_subplot(111)
        self.axes.set_xlim([0, 1])
        self.axes.set_ylim([0, 1])

        name = self.display_name(kwargs.get('cap')) if 'cap' in kwargs else 'Raster Spike'
        self.axes.set_title(name)
