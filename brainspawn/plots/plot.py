""" Module for plots. Plots with one matplotlib subplot should extend from
this class. Otherwise if multiple plots are needed, must extend from actual
BasePlot.
"""

import gtk
from abc import ABCMeta, abstractmethod
from plots.base_plot import BasePlot
from plots.configuration import Configuration
import settings


class Plot(BasePlot):
    """Plot class.
    In order to add plots to the visualizer, you will want to
    inherit from this class.

    Note that subclasses must call the base class constructor.
    """

    __metaclass__ = ABCMeta

    def __init__(self, main_controller, nengo_obj, capability):
        super(Plot, self).__init__(main_controller, nengo_obj, capability)
        """ Plot constructor.
        Initializes default config values for all plots, and sets up the plot
        view.

        Args:
            main_controller (VisualizerController): The top-level controller
            of the visualizer.
            nengo_obj (Nengo): The nengo object this plot is visualizing.
            capability (Capability): The capability of the object that this
            graph is visualizing.
            config (dict): saved config options for the plot.
        """

        self.axes = self.figure.add_subplot(111)
        self.axes.patch.set_alpha(0.0)

        self.init_default_config()

    def init_default_config(self):
        """ Sets default config values for all plots.
        The values contained in this dictionary are used to configure the plot.

        For convenience in title string formatting,
        we set 'TARGET' and 'DATA' to default values of the
        target object, and represented data, respectively.
        """
        super(Plot, self).init_default_config()

        self.config['title'] = Configuration(
            configurable=True, display_name="Title", data_type='text',
            value='{TARGET} - {DATA}', function=self.set_title)

    def set_title(self, title):
        """ Returns the title.
        """
        self.axes.set_title(self.title)

    def set_default_xlim(self, end_time, x_width):
        """ Sets x axes to be a constant width, meaning it won't change in
        scale.
        """
        if end_time > x_width:
            self.axes.set_xlim([end_time - x_width, end_time])
        else:
            self.axes.set_xlim([0, x_width])
