"""Base class for all plot views
"""

import gtk
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
import plots.network_view

class PlotView(object):

    def __init__(self, controller):
        self._figure = Figure()
        self._figure.patch.set_alpha(0.0)
        self._canvas = FigureCanvas(self._figure)
        self.context_menu = gtk.Menu()
        self._canvas.connect("button_release_event", controller.button_press, self._canvas)

        # Context menu setup
        export_pdf_item = gtk.MenuItem("Export to PDF...")
        export_pdf_item.connect("activate", controller.on_export_pdf, self._canvas)
        self.context_menu.append(export_pdf_item)

        remove_item = gtk.MenuItem("Remove")
        remove_item.connect("activate", controller.remove_plot, self._canvas)
        if (not isinstance(controller, plots.network_view.NetworkView)):
            self.context_menu.append(remove_item)

        self.context_menu.show_all()

    @property
    def figure(self):
        return self._figure

    @property
    def canvas(self):
        return self._canvas

