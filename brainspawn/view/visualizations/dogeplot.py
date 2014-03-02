import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from view.visualizations.__visualization import Visualization

def class_name():
    return "DogePlot"

class DogePlot(Visualization):
    """DogePlot
    """

    def name(self):
        return "Doge Plot"

    def __init__(self, sim_manager, main_controller, name="Doge Plot", dimensions=2, xlabel='x', title='XY Plot',
            *args, **kwargs):
        #self.i = 0
        self.sim_manager  = sim_manager
        self.main_controller = main_controller
        self._figure = plt.figure()
        self.init_canvas(self._figure)
        self._figure.patch.set_facecolor('white')

        start = self.sim_manager.min_step
        count = self.sim_manager.current_step - self.sim_manager.min_step

        self.lines = plt.plot([], np.empty((0, dimensions)))
        self.text = []
        plt.ylabel('time')
        plt.xlabel(xlabel)
        plt.title(title)

    def display_name(self):
        return "so science"

    def supports_cap(self, cap, dimensions):
        return cap.name() is "voltages" or cap.name() is "output"

    def update(self, data, start_time):
        """ Update x data for each line in graph
        """
        buffer_start = start_time/self.sim_manager.dt
        count = self.sim_manager.current_step - buffer_start
        t = np.linspace(buffer_start,
                buffer_start + data[buffer_start:count].shape[0]*self.sim_manager.dt,
                data[buffer_start:count].shape[0])

        if(not self.text and len(t) > 10):
            self.text.append(plt.text(0.27, 0.77, "such line", fontsize=12, color='orange'))
            self.text.append(plt.text(0.7, 0.57, "very neuron", fontsize=12, color='green'))
            self.text.append(plt.text(0.77, 0.2, "wow", fontsize=12, color='purple'))
            self.text.append(plt.text(0.07, 0.32, "so science", fontsize=12, color='cyan'))
        elif (self.text and len(t) < 275):
            for txt in self.text:
                txt.set_x((txt.get_position()[0]*100000 + len(t))/100000 % 1 )

        for idx, line in enumerate(self.lines):
            line.set_xdata(t)
            line.set_ydata(data[buffer_start:count,idx:idx+1])

    def clear(self):
        for line in self.lines:
            line.set_xdata([])
            line.set_ydata([])

