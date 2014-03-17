""" Abstract base class for plots.
"""

from abc import ABCMeta, abstractmethod
from views.plot_view import PlotView
from collections import OrderedDict

REGISTERED_PLOTS = {}

def registered_plot(cls):
    """Decorator for plot implementations.
    """
    REGISTERED_PLOTS[cls.__name__] = cls
    return cls

class Plot(object):
    """Plot base class.
    In order to add plots to Brainspawn, you will want to
    inherit from this class.

    Note that subclasses must call the base class constructor.
    """

    __metaclass__ = ABCMeta

    def __init__(self, main_controller, nengo_obj, capability):
        """ Plot constructor.
        Initializes default config values for all plots,
        Sets up the plot view and axes.

        Args:
            main_controller (VisualizerController): The top-level controller
            of the visualizer.
            nengo_obj (Nengo): The nengo object this plot is visualizing.
            capability (Capability): The capability of the object that this graph
            is visualizing.
        """
        self.main_controller = main_controller
        self.nengo_obj = nengo_obj
        self.capability = capability
        self.config = {}
        self.init_default_config(nengo_obj, capability)

        self.view = PlotView(self)
        self.axes = self.view.figure.add_subplot(111) # take first from list
        self.axes.set_title(self.title)

    def init_default_config(self, nengo_obj, capability):
        """Sets default config values for all plots
        The values contained in this dictionary are used to configure
        the plot.

        For convenience in title string formatting,
        we set 'TARGET' and 'DATA' to default values of the
        target object, and represented data, respectively.
        """
        if not nengo_obj or not capability:
            return
        self.config['title'] = '{TARGET} - {DATA}'
        self.config['TARGET'] = nengo_obj.label
        self.config['DATA'] = capability.name

    @property
    def title(self):
        """ Return a title for the current graph.
        Format the string using self.config as the format dictionary.

        Returns:
            string. A string to use as the title of the current graph.

        Note the availability of TARGET and DATA for use in the title
        format string.
        """
        try:
            title = self.config['title'].format(**self.config)
        except KeyError as e:
            title = self.plot_name()
        return title

    @property
    def dimensions(self):
        """Get the dimensions of the object this graph is representing.

        Returns:
            int. The ouput dimensions we are plotting.
        """
        return self.capability.get_out_dimensions(self.nengo_obj)

    @staticmethod
    def plot_name():
        """ What we call the plot.
        (Used when choosing plot from dropdown menu)
        """
        raise NotImplementedError("Not implemented")

    @staticmethod
    def supports_cap(capability):
        """ Return true if this plot supports the given capability.

        Args:
            capability (Capablility): The capability to check for plotability.
        """
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def update(self, start_step, step_size, data):
        """ Callback function passed to observer nodes.

        Args:
            start_step (int): The initial step of the given data.
            step_size (int): The time, in simulated seconds, one step represents.
            data (int): The data from the simulator to plot.
        """
        pass
    
    def get_options_dict(self):
        pass
        #return OrderedDict([
        #        ('Title', ('string', 'text', self.axes.set_title))
        #        ])

    def remove_plot(self, widget, canvas):
        self.main_controller.remove_plot_for_obj(self, self.nengo_obj, self.capability)

    def on_export_pdf(self, widget, canvas):
        self.main_controller.on_export_pdf(None, canvas, self.title)

    def button_press(self, widget, event, canvas):
        if event.button == 3:
            self.view.context_menu.popup(None, None, None, None, event.button, event.time)
            return True
        return False

