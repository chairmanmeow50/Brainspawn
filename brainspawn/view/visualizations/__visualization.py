""" Abstract base class for Visualizations
"""

import gtk
from abc import ABCMeta, abstractmethod
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

class Visualization(object):
    """Visualization class
    """

    __metaclass__ = ABCMeta

    def __init__(self, sim_manager, main_controller, cap=None):
        self.sim_manager = sim_manager
        self.main_controller = main_controller
        self.customize_windows = []
        self._cap = cap

    @property
    def figure(self):
        return self._figure

    @property
    def canvas(self):
        return self._canvas

    @staticmethod
    def display_name(cap):
        """ Name of graph for given cap
        """
        raise NotImplementedError("Not implemented")

    @staticmethod
    def supports_cap(cap, dimension):
        """ Return true if supports cap
        """
        raise NotImplementedError("Not implemented")

    def set_cap(self, cap):
        self._cap = cap

    def update(self, data, start_time):
        """ Callback function passed to observer nodes
        """
        pass

    @abstractmethod
    def clear(self):
        """ Clear the graph
        """
        pass

    def init_canvas(self, figure):
        self._canvas = FigureCanvas(figure)
        self._canvas.connect("button_release_event", self.button_press, self._canvas)

    def button_press(self, widget, event, canvas):
        if event.button == 3:
            export_pdf_item = gtk.MenuItem("Export to PDF...")
            export_pdf_item.connect("activate", self.on_export_pdf, canvas)
            remove_item = gtk.MenuItem("Remove")
            remove_item.connect("activate", self.remove_plot, canvas)
            self.context_menu = gtk.Menu()
            self.context_menu.append(export_pdf_item)
            self.context_menu.append(remove_item)
            self.context_menu.show_all()
            self.context_menu.popup(None, None, None, None, event.button, event.time)
            return True
        return False
    
    def remove_plot(self, widget, canvas):
        if (self._cap):
            self.sim_manager.disconnect_from_obj(self.main_controller.obj, self._cap, self.update)
            self.main_controller.main_frame.remove_plot(self)

    def on_export_pdf(self, widget, canvas):
        filename = self.main_controller.file_browse(gtk.FILE_CHOOSER_ACTION_SAVE, "screenshot.pdf")
        if not filename:
            return
        with open(filename, "wb") as f:
            canvas.figure.patch.set_facecolor('white')
            canvas.print_pdf(f)
