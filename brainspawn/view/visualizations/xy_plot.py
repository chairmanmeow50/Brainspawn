import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from view.visualizations.__visualization import Visualization

def class_name():
    return "XY_Plot"

class XY_Plot(Visualization):
    """XY Plot
    """

    def __init__(self, sim_manager, name, dimensions, xlabel='x', title='XY Plot', *args, **kwargs):
        self.sim_manager  = sim_manager
        self._figure = plt.figure()
        self.init_canvas(self._figure)
        self._figure.patch.set_facecolor('white')

        start = self.sim_manager.min_step
        count = self.sim_manager.current_step - self.sim_manager.min_step

        self.lines = plt.plot([], np.empty((0, dimensions)))
        plt.ylabel('time')
        plt.xlabel(xlabel)
        plt.title(title)

    def update(self, data, start_time):
        """ Update x data for each line in graph
        """
        buffer_start = start_time/self.sim_manager.dt
        count = self.sim_manager.current_step - buffer_start
        t = np.linspace(buffer_start,
                buffer_start + data[buffer_start:count].shape[0]*self.sim_manager.dt,
                data[buffer_start:count].shape[0])

        for idx, line in enumerate(self.lines):
            line.set_xdata(t)
            line.set_ydata(data[buffer_start:count,idx:idx+1])

    def clear(self):
        for line in self.lines:
            line.set_xdata([])
            line.set_ydata([])

