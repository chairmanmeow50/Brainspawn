import numpy as np
from view.visualizations.__visualization import Visualization

def class_name():
    return "XYPlot"

class XYPlot(Visualization):
    """XY Plot
    """

    def __init__(self, main_controller, obj, cap):
        super(XYPlot, self).__init__(main_controller, obj, cap)

        self.lines = self.axes.plot([], np.empty((0, self.dimensions)))
        self.axes.set_ylabel('time')
        self.axes.yaxis.set_label_coords(-0.05, 0.5)
        self.axes.set_xlabel('xlabel')
        self.axes.xaxis.set_label_coords(0.5, -0.05)
        self.axes.set_ylim([0, 1])
        self.axes.set_xlim([0, 1])

    @staticmethod
    def plot_name():
        return "XY Plot"

    @staticmethod
    def supports_cap(cap):
        return cap.name in ['voltages', 'output']

    def update(self, start_step, step_size, data):
        """ Update x data for each line in graph
        """
        start_time = start_step*step_size
        end_time = (start_step + data.shape[0])*step_size

        t = np.linspace(start_time, end_time, data.shape[0])

        for idx, line in enumerate(self.lines):
            line.set_xdata(t)
            line.set_ydata(data[:,idx:idx+1])

        if end_time > 1:
            self.axes.set_xlim([t[0], t[-1]])
        else:
            self.axes.set_xlim([0, 1])

        if len(data) > 0:
            self.axes.set_ylim([min(np.amin(data), 0), max(np.amax(data), 1)])

