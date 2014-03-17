""" Abstract base class for plots.
"""

import gtk
from abc import ABCMeta, abstractmethod
from plots.base_plot import BasePlot
from plots.configuration import Configuration

class Plot(BasePlot):
    """Plot class.
    In order to add plots to Brainspawn, you will want to
    inherit from this class.

    Note that subclasses must call the base class constructor.
    """

    __metaclass__ = ABCMeta

    def __init__(self, main_controller, nengo_obj, capability, config=None):
        super(Plot, self).__init__(main_controller, nengo_obj, capability, config)
        """ Plot constructor.
        Initializes default config values for all plots,
        Sets up the plot view.

        Args:
            main_controller (VisualizerController): The top-level controller
            of the visualizer.
            nengo_obj (Nengo): The nengo object this plot is visualizing.
            capability (Capability): The capability of the object that this graph
            is visualizing.
            config (dict): saved config options for the plot
        """

        self.axes = self.figure.add_subplot(111)
        self.axes.patch.set_alpha(0.0)
        self.axes.set_title(self.title)

    def init_default_config(self, nengo_obj, capability):
        """Sets default config values for all plots
        The values contained in this dictionary are used to configure
        the plot.

        For convenience in title string formatting,
        we set 'TARGET' and 'DATA' to default values of the
        target object, and represented data, respectively.
        """
        super(Plot, self).init_default_config(nengo_obj, capability)
        if not nengo_obj or not capability:
            return

        self.config['title'] = Configuration(
                                      configurable = True,
                                      display_name = "Title",
                                      data_type = 'text',
                                      value = '{TARGET} - {DATA}',
                                      function = self.set_title)

    def set_title(self, title):
        self.axes.set_title(title)
