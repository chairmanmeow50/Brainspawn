""" Abstract base class for Visualizations
"""

import gtk
from abc import ABCMeta, abstractmethod
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

class Visualization(object):
    """Visualization class
    """

    __metaclass__ = ABCMeta

    def __init__(self, sim_manager, main_controller):
        self.sim_manager = sim_manager
        self.main_controller = main_controller

    @property
    def figure(self):
        return self._figure

    @property
    def canvas(self):
        return self._canvas

    @abstractmethod
    def display_name(self):
        pass

    @abstractmethod
    def supports_cap(self, cap, dimension):
        pass

    @abstractmethod
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
        self._canvas.connect("event", self.button_press, self._canvas)

    def button_press(self, widget, event, canvas):
        if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
            export_pdf_item = gtk.MenuItem("Export to PDF")
            export_pdf_item.connect("activate", self.on_export_pdf, canvas)
            export_pdf_item.show()
            context_menu = gtk.Menu()
            context_menu.append(export_pdf_item)
            context_menu.popup(None, None, None, event.button, event.time)
            return True
        return False

    def on_export_pdf(self, widget, canvas):
        filename = self.main_controller.file_browse(gtk.FILE_CHOOSER_ACTION_SAVE, "screenshot.pdf")
        if not filename:
            return
        with open(filename, "wb") as f:
            if canvas:
                canvas.print_pdf(f)

