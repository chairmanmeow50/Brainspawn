""" Abstract base class for items we put on the canvas.
"""

import gtk
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as \
    FigureCanvas
from collections import OrderedDict
from views.components.customize_window import CustomizeWindow
import settings

class CanvasItem(object):
    """Canvas Item
    Has figure, canvas
    """

    def __init__(self, main_controller):
        """ Initializes figure. Sets a default alpha. Initializes 
        configuration dictionary. Initializes context menu. Connects 
        button release event on canvas.
        """
        self.main_controller = main_controller
        self.figure = Figure()
        self.figure.patch.set_alpha(0.0)
        self.canvas = FigureCanvas(self.figure)
        
        self.customize_window = None
        self.config = OrderedDict()

        self._context_menu = gtk.Menu()
        self._build_context_menu()
        self.canvas.connect("button_release_event", self.on_button_release, 
                            self.canvas)

    def _build_context_menu(self):
        """ Context menu has menu items for exporting to PDF 
        and customizing plot.
        """
        export_pdf_item = gtk.MenuItem("Export to PDF...")
        export_pdf_item.connect("activate", self.on_export_pdf, self.canvas)
        customize_item = gtk.MenuItem("Customize...")
        customize_item.connect("activate", self.show_customize)

        self._context_menu.append(export_pdf_item)
        self._context_menu.append(customize_item)

        self._context_menu.show_all()

    def init_default_config(self):
        """ Empty abstract default config.
        """
        pass
    
    def get_options_dict(self):
        """ Return configuration dictionary.
        """
        return self.config

    def get_config_values(self):
        """ Gets values of all items in configuration dictionary.
        Returns values as keys in new dictionary.
        """
        return {key : configuration.value for key, configuration in \
                self.config.iteritems()}

    def set_config_values(self, config):
        """ Sets current configuration values to ones from 
        configuration dictionary in parameter.
        """
        if (config):
            for key, val in config.items():
                self.config[key].value = val
            
    def apply_config(self, revert_data=None, get_function=None):
        """ For each configuration, if revert data exists,
        revert configuration. If no revert data is provided, 
        set configuration value to result from get function. 
        If no get function is specified, use current value from 
        configuration.
        
        Calls the function within the configuration with the 
        revert/get function/current value.
        
        Calls queue_draw to update after applying configuration.
        """
        for option_name in self.get_options_dict():
            if (self.config[option_name].configurable):
                if (self.config[option_name].function):
                    function = self.config[option_name].function
                    if (revert_data):
                        new_val = revert_data[option_name]
                    elif (get_function):
                        new_val = get_function(option_name)
                    else:
                        new_val = self.config[option_name].value
                        
                    self.config[option_name].value = new_val
                    function(new_val)
        
        self.canvas.queue_draw()

    @property
    def title(self):
        """ Abstract title getter.
        """
        raise NotImplementedError

    def on_export_pdf(self, widget, canvas):
        """ Calls controller's export pdf function with plot title.
        """
        self.main_controller.on_export_pdf(None, canvas, self.title)

    def on_button_release(self, widget, event, canvas):
        """ TODO: is this needed for some behavoiur?
        ie. the disappearing context menu.
        """
        if event.button == settings.EVENT_BUTTON_RIGHT_CLICK:
            self._context_menu.popup(None, None, None, None, event.button, \
                                     event.time)
            return True
        return False

    def show_customize(self, event):
        """ If plot has customize window already, show that menu.
        Else, instantiate new customize window and show it.
        """
        if (self.customize_window and self.customize_window.not_destroyed):
            self.customize_window.window.show()
        else:
            self.customize_window = CustomizeWindow(self)
