""" Abstract base class for items we put on the canvas
"""

import gtk
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from collections import OrderedDict
from plots.configuration import Configuration
from views.components.customize_window import CustomizeWindow

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
        self.customize_window = None
        self.config = OrderedDict()

        self._context_menu = gtk.Menu()
        self._build_context_menu()
        self.canvas.connect("button_release_event", self.on_button_release, self.canvas)

    def _build_context_menu(self):
        """Context menu setup
        """
        export_pdf_item = gtk.MenuItem("Export to PDF...")
        export_pdf_item.connect("activate", self.on_export_pdf, self.canvas)
        
        customize_item = gtk.MenuItem("Customize")
        customize_item.connect("activate", self.show_customize)
        
        self._context_menu.append(export_pdf_item)
        self._context_menu.append(customize_item)

        self._context_menu.show_all()
        
    def init_default_config(self, nengo_obj, capability):
        pass
    
    def get_config_values(self):
        return {key : configuration.value for key, configuration in self.config.iteritems()}

    def set_config_values(self, config):
        if (config):
            for key, val in config.items():
                #self.config[key].value = val
                pass

    def on_export_pdf(self, widget, canvas):
        self.main_controller.on_export_pdf(None, canvas, self.title)

    def on_button_release(self, widget, event, canvas):
        if event.button == 3:
            self._context_menu.popup(None, None, None, None, event.button, event.time)
            return True
        return False

    def show_customize(self, event):
        if (self.customize_window and self.customize_window.not_destroyed):
            self.customize_window.window.show()
        else:
            self.customize_window = CustomizeWindow(self)
            