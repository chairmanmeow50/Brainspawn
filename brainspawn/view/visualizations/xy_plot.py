import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from view.visualizations.__visualization import Visualization

def class_name():
    return "XYPlot"

class XYPlot(Visualization):
    """XY Plot
    """

    def __init__(self, sim_manager, controller, **kwargs):
        super(XYPlot, self).__init__(sim_manager, controller)
        self._figure = plt.figure()
        self.init_canvas(self._figure)
        self._figure.patch.set_facecolor('white')

        start = self.sim_manager.min_step
        count = self.sim_manager.current_step - self.sim_manager.min_step

        if 'dimensions' in kwargs:
            self.dimensions = kwargs.get('dimensions')
        else:
            self.dimensions = 1
        self.lines = plt.plot([], np.empty((0, self.dimensions)))
        self.axes = plt.gca()
        plt.ylabel('time')
        plt.xlabel('xlabel')
        plt.title("XY Plot")
        self.axes.set_ylim([0, 1])
        self.axes.set_xlim([0, 1])

    @staticmethod
    def display_name(cap):
        return "XY Plot" + " " + cap.name

    @staticmethod
    def supports_cap(cap, dimensions):
        return cap.name in ['voltages', 'output']

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

        if count*self.sim_manager.dt > 1:
            self.axes.set_xlim([start_time, start_time + count*self.sim_manager.dt])

    def clear(self):
        for line in self.lines:
            line.set_xdata([])
            line.set_ydata([])

