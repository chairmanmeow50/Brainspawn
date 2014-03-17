import numpy as np
from plots.plot import Plot
from plots.base_plot import registered_plot
from plots.configuration import Configuration

@registered_plot
class ValuePlot(Plot):
    """Graph for plotting values over time.
    """

    def __init__(self, main_controller, nengo_obj, capability, config=None):
        """
        Set up the plot, and axis labels.

        Args:
            main_controller (VisualizerController): The top-level controller
            of the visualizer.
            nengo_obj (Nengo): The nengo object this plot is visualizing.
            capability (Capability): The capability of the object that this graph
            is visualizing.

        Note the call to super constructor.
        """
        super(ValuePlot, self).__init__(main_controller, nengo_obj, capability, config)

        self.init_default_config(nengo_obj, capability)
        self.axes.set_ylabel(self.config['DATA'].value)
        self.axes.set_xlabel('Time (s)')
        self.axes.set_xlim([0, 1])
        self.axes.patch.set_alpha(1.0)

        self.lines = self.axes.plot([], np.empty((0, self.dimensions)))

    @staticmethod
    def plot_name():
        """ What we call the plot.
        (Used when choosing plot from dropdown menu)

        Returns:
            string. The plot name.
        """
        return "Value"

    @staticmethod
    def supports_cap(cap):
        """ Return true if this plot supports the given capability.

        Args:
            capability (Capablility): The capability to check for plotability.

        Returns:
            bool. True if this plot supports the given capability.
        """
        return cap.name in ['voltages', 'output']

    def get_options_dict(self):
        self.config['xlabel'] = Configuration(
                                              configurable = True,
                                              display_name = "X Label",
                                              data_type = "text",
                                              value = "time",
                                              function = self.axes.set_xlabel)
        
        self.config['ylabel'] = Configuration(
                                              configurable = True,
                                              display_name = "Y Label",
                                              data_type = "text",
                                              value = self.config['DATA'].value,
                                              function = self.axes.set_ylabel)
        
        self.config['ylabel'] = Configuration(
                                              configurable = True,
                                              display_name = "X Scale",
                                              data_type = "combo",
                                              value = 'linear',
                                              function = self.axes.set_xscale,
                                              combo = ['linear', 'log', 'symlog'])
        
        self.config['frame'] = Configuration(
                                             configurable = True,
                                             display_name = "Frame",
                                             data_type = "boolean",
                                             value = True,
                                             function = self.axes.set_frame_on)
        
        self.config['axes_bg_color'] = Configuration(
                                                     configurable = True,
                                                     display_name = "Axis Background Color",
                                                     data_type = "color",
                                                     value = "#FFFFFF",
                                                     function = self.axes.set_axis_bgcolor)
        
        return self.config

    def update(self, start_step, step_size, data):
        """ Callback function passed to observer nodes.

        Update x data for each line in graph, and autoscale axis limits as needed

        Args:
            start_step (int): The initial step of the given data.
            step_size (int): The time, in simulated seconds, one step represents.
            data (int): The data from the simulator to plot.
        """
        start_time = start_step*step_size
        end_time = (start_step + data.shape[0])*step_size

        t = np.linspace(start_time, end_time, data.shape[0])

        for idx, line in enumerate(self.lines):
            line.set_xdata(t)
            line.set_ydata(data[:,idx:idx+1])

        self.axes.relim()
        self.axes.autoscale_view(tight=True)

        if end_time > 1 and len(t) > 1:
            self.axes.set_xlim([t[0], t[-1]])
        else:
            self.axes.set_xlim([0, 1])

