import numpy as np
from plots.plot import Plot, registered_plot

@registered_plot
class TutorialPlotV1(Plot):
    """Graph for plotting values over time.
    """

    def __init__(self, main_controller, nengo_obj, capability):
        """
        Set up the plot, and axis labels and limits.

        Args:
            main_controller (VisualizerController): The top-level controller
            of the visualizer.
            nengo_obj (Nengo): The nengo object this plot is visualizing.
            capability (Capability): The capability of the object that this graph
            is visualizing.

        Note the call to super constructor.
        """
        super(TutorialPlotV1, self).__init__(main_controller, nengo_obj, capability)

        # TODO - Let's get rid of this and initialize the plot again, but this time with empty data
        # Hint - Keep track of the lines axes.plot() returns, you can update them later!
        self.lines = self.axes.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 1, 2, 3, 5, 8, 13, 21, 34, 55])

        self.axes.set_ylabel(self.config['DATA'])
        self.axes.set_xlabel('time')

    @staticmethod
    def plot_name():
        """ What we call the plot.
        (Used when choosing plot from dropdown menu)

        Returns:
            string. The plot name.
        """
        return "Tutorial Plot V1"

    @staticmethod
    def supports_cap(cap):
        """ Return true if this plot supports the given capability.

        Args:
            capability (Capablility): The capability to check for plotability.

        Returns:
            bool. True if this plot supports the given capability.
        """
        return cap.name in ['voltages', 'output']

    def update(self, start_step, step_size, data):
        """ Callback function passed to observer nodes.

        Update x data for each line in graph, and autoscale axis limits as needed

        Args:
            start_step (int): The initial step of the given data.
            step_size (float): The time, in simulated seconds, one step represents.
            data (numpy.ndarray): The data from the simulator to plot.
        """

        # TODO - We can calculate the start and end times in simulated seconds

        # TODO - With that, let's create the new time series for the xdata

        # TODO - Finally, let's update the lines of the plot with the new data



