""" Abstract base class for items we put on the canvas
"""

import gtk
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

class CanvasItem(object):
    """Canvas Item
    Has figure, canvas
    """

    def __init__(self, main_controller):
        """ Constructor.
        """
        self.main_controller = main_controller
        self.figure = Figure()
        self.figure.patch.set_alpha(0.0)
        self.canvas = FigureCanvas(self.figure)

        self._context_menu = gtk.Menu()
        self._build_context_menu()
        self.canvas.connect("button_release_event", self.button_press, self.canvas)

    def _build_context_menu(self):
        """Context menu setup
        """
        export_pdf_item = gtk.MenuItem("Export to PDF...")
        export_pdf_item.connect("activate", self.on_export_pdf, self.canvas)
        self._context_menu.append(export_pdf_item)

        self._context_menu.show_all()

    def on_export_pdf(self, widget, canvas):
        self.main_controller.on_export_pdf(None, canvas, self.title)

    def button_press(self, widget, event, canvas):
        if event.button == 3:
            self._context_menu.popup(None, None, None, None, event.button, event.time)
            return True
        return False

