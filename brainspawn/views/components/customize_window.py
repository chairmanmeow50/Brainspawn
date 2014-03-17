import gtk
from gi.repository import Gtk

class CustomizeWindow:
    def __init__(self, plot, **kwargs):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        #self.window.set_default_size(640, 480)
        self.plot = plot
        name = "Customize " + kwargs.get('name') if 'name' in kwargs else "Customize"
        self.window.set_title(name)
        
        self.options = plot.get_options_dict()
        
        self.vbox = gtk.VBox()
        self.controls = {}
        control = None
        
        for option_name in self.options:
            if (self.options[option_name].configurable):
                data_type = self.options[option_name].data_type
                text_label = gtk.Label(self.options[option_name].display_name)
                type_label = gtk.Label(data_type)
                
                if (data_type == 'text'):
                    control = gtk.Entry()
                    control.set_text(self.options[option_name].value)
                    control.connect("changed", self.apply_all)
                
                if (control):
                    self.controls[option_name] = control
                    
                    hbox = Gtk.HBox(True, 10)
                    hbox.pack_start(text_label, True, True, 10)
                    hbox.pack_start(type_label, True, True, 10)
                    hbox.pack_start(control, True, True, 10)
                    
                    self.vbox.pack_start(hbox, True, False, 10)

        apply_button = gtk.Button(label="Apply")
        apply_button.connect("clicked", self.apply_all)
        self.vbox.pack_start(apply_button)
        self.window.add(self.vbox)
        self.window.show_all()
    
    def apply_all(self, widget):
        for option_name in self.options:
            if (self.options[option_name].function):
                function = self.options[option_name].function
                function(self.get_val(option_name))
        
        self.plot.canvas.queue_draw()
            
    def get_val(self, option_name):
        data_type = self.options[option_name].data_type
        if (data_type == 'text'):
            unformatted_string = self.controls[option_name].get_text()
            config_values = self.plot.get_config_values()
            try:
                formatted_string = unformatted_string.format(**config_values)
                return formatted_string
            except (KeyError, ValueError) as e:
                return unformatted_string