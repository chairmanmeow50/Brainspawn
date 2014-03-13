import numpy as np
from plots.plot import Plot, registered_plot

@registered_plot
class TutorialPlot(Plot):
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
        super(TutorialPlot, self).__init__(main_controller, nengo_obj, capability)

        # TODO - Let's just plot some arbitrary data onto the axis for now

        # TODO - Let's give the axes some labels

    @staticmethod
    def plot_name():
        """ What we call the plot.
        (Used when choosing plot from dropdown menu)

        Returns:
            string. The plot name.
        """
        return "Tutorial Plot"

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
            step_size (int): The time, in simulated seconds, one step represents.
            data (int): The data from the simulator to plot.
        """
        # We don't need to do anything here yet,
        pass

