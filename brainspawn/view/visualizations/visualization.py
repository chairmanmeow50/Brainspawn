""" Abstract base class for Visualizations
"""

import gtk
from abc import ABCMeta, abstractmethod
from view.visualizations.plot_view import PlotView

registered_plots = []

def registered_plot(cls):
    """Decorator for visualization implementations
    In order to be accessible by import *, must also add to __all__ in __init__.py
    """
    registered_plots.append(cls)
    return cls

class Visualization(object):
    """Visualization class
    """

    __metaclass__ = ABCMeta

    def __init__(self, main_controller, obj, cap):
        self.main_controller = main_controller
        self._obj = obj
        self._cap = cap
        self.config = {}
        self.init_default_config(obj, cap)

        self.view = PlotView(self)
        self.axes = self.view.figure.add_subplot(111) # take first from list
        self.axes.set_title(self.title)

    def init_default_config(self, obj, cap):
        """For convenience in title string formatting,
        we set 'TARGET' and 'DATA' to default values of the
        target object, and represented data, respectively
        """
        if not obj or not cap:
            return
        self.config['title'] = '{TARGET} - {DATA}'
        self.config['TARGET'] = obj.label
        self.config['DATA'] = cap.name

    @property
    def title(self):
        """ Return a title for the current graph
        Format the string, config is passed in as kwargs
        """
        try:
            title = self.config['title'].format(**self.config)
        except KeyError as e:
            title = self.plot_name()
        return title

    @property
    def dimensions(self):
        """Return the dimensions of the object this graph is representing
        """
        return self._cap.get_out_dimensions(self._obj)

    @staticmethod
    def plot_name():
        """ What we call the plot
        (Used when choosing plot from dropdown menu)
        """
        raise NotImplementedError("Not implemented")

    @staticmethod
    def supports_cap(cap):
        """ Return true if supports cap
        """
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def update(self, start_step, step_size, data):
        """ Callback function passed to observer nodes
        """
        pass

    def remove_plot(self, widget, canvas):
        self.main_controller.remove_plot_for_obj(self, self._obj, self._cap)

    def on_export_pdf(self, widget, canvas):
        filename = self.main_controller.file_browse(gtk.FILE_CHOOSER_ACTION_SAVE, self.title + ".pdf")
        if not filename:
            return
        with open(filename, "wb") as f:
            canvas.print_pdf(f)

    def button_press(self, widget, event, canvas):
        if event.button == 3:
            self.view.context_menu.popup(None, None, None, None, event.button, event.time)
            return True
        return False

