import numpy as np
from plots.plot import Plot, registered_plot

@registered_plot
class ValuePlot(Plot):
    """Graph for plotting values over time
    """

    def __init__(self, main_controller, nengo_obj, capability):
        """
        Set up the plot, and axis labels and limits

        Args:
            main_controller (VisualizerController): The top-level controller
            of the visualizer
            nengo_obj (Nengo): The nengo object this plot is visualizing
            capability (Capability): The capability of the object that this graph
            is visualizing

        Note the call to super constructor
        """
        super(ValuePlot, self).__init__(main_controller, nengo_obj, capability)

        self.lines = self.axes.plot([], np.empty((0, self.dimensions)))
        self.axes.set_ylabel(self.config['DATA'])
        self.axes.set_xlabel('time')
        self.axes.set_ylim([0, 1])
        self.axes.set_xlim([0, 1])

    @staticmethod
    def plot_name():
        """ What we call the plot
        (Used when choosing plot from dropdown menu)

        Returns:
            string. The plot name
        """
        return "Value Plot"

    @staticmethod
    def supports_cap(cap):
        """ Return true if this plot supports the given capability

        Args:
            capability (Capablility): The capability to check for plotability

        Returns:
            bool. True if this plot supports the given capability
        """
        return cap.name in ['voltages', 'output']

    def update(self, start_step, step_size, data):
        """ Callback function passed to observer nodes

        Update x data for each line in graph, and update axis limits as needed

        Args:
            start_step (int): The initial step of the given data
            step_size (int): The time, in simulated seconds, one step represents
            data (int): The data from the simulator to plot
        """
        start_time = start_step*step_size
        end_time = (start_step + data.shape[0])*step_size

        t = np.linspace(start_time, end_time, data.shape[0])

        for idx, line in enumerate(self.lines):
            line.set_xdata(t)
            line.set_ydata(data[:,idx:idx+1])

        if end_time > 1 and len(t) > 1:
            self.axes.set_xlim([t[0], t[-1]])
        else:
            self.axes.set_xlim([0, 1])

        if len(data) > 0:
            data_max = np.amax(data)
            data_min = np.amin(data)
            if data_max != data_min:
                self.axes.set_ylim([min(data_min, 0), max(data_max, 1)])
