import gtk
from gi.repository import Gtk

class CustomizeWindow:
    def __init__(self, plot, **kwargs):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_border_width(10)
        self.window.set_resizable(False)
        self.plot = plot
        self.window.set_title("Customize")
        
        self.options = plot.get_options_dict()
        
        self.vbox = gtk.VBox()
        self.controls = {}
        self.revert_data = {}
        control = None
        
        if (self.options):
            for option_name in self.options:
                if (self.options[option_name].configurable):
                    data_type = self.options[option_name].data_type
                    text_label = gtk.Label(self.options[option_name].display_name)
                    self.revert_data[option_name] = self.options[option_name].value
                    
                    if (data_type == 'text'):
                        control = gtk.Entry()
                        control.set_text(self.options[option_name].value)
                    elif (data_type == 'combo'):
                        control = Gtk.ComboBoxText()
                        combo_values = self.options[option_name].combo
                        for combo_value in combo_values:
                            control.append(combo_value, combo_value)
                        control.set_entry_text_column(0)
                        
                        control.set_active(combo_values.index(self.options[option_name].value))
                    elif (data_type == 'boolean'):
                        control = Gtk.CheckButton()
                        control.set_active(self.options[option_name].value)
                    elif (data_type == 'color'):
                        control = Gtk.Button("Color chooser...")
                        
                        color_selection_dialog = Gtk.ColorSelectionDialog()
                        control.connect("clicked", self.show_color_selection_dialog, color_selection_dialog)
                        color_selection = color_selection_dialog.get_color_selection()
                        self.controls[option_name] = color_selection
                        color_selection.connect("color_changed", self.apply_all)
                    elif (data_type == 'slider'):
                        slider_adjustment = Gtk.Adjustment()
                        control = Gtk.HScale(adjustment = slider_adjustment)
                        (min, max) = self.options[option_name].bounds
                        slider_adjustment.set_lower(min)
                        slider_adjustment.set_upper(max)
                        slider_adjustment.set_value(self.options[option_name].value)
                        self.controls[option_name] = control
                        slider_adjustment.connect("value_changed", self.apply_all)
                                
                    if (control):
                        if (data_type == 'text' or data_type == 'combo'):
                            control.connect("changed", self.apply_all)
                        elif (data_type == 'boolean'):
                            control.connect("toggled", self.apply_all)
                            
                        if (data_type != 'color' and data_type != 'slider'):
                            self.controls[option_name] = control
                        
                        hbox = Gtk.HBox(True, 5)
                        text_label.set_alignment(1, 0.5)
                        hbox.pack_start(text_label, True, True, 5)
                        hbox.pack_start(control, True, True, 5)
                        
                        self.vbox.pack_start(hbox, True, False, 10)

        ok_button = gtk.Button(label="Ok")
        ok_button.connect("clicked", self.ok_clicked)
        ok_button.set_size_request(80, 20)
        
        revert_button = gtk.Button(label="Revert")
        revert_button.connect("clicked", self.revert_all)
        revert_button.set_size_request(80, 20)
        
        button_hbox = Gtk.Box(Gtk.Orientation.HORIZONTAL, 20)
        button_hbox.set_homogeneous(True)
        
        alignment = Gtk.Alignment()
        alignment.set(0.5, 1, 0, 0)
        alignment.add(button_hbox)
        
        button_hbox.pack_end(ok_button, False, False)
        button_hbox.pack_end(revert_button, False, False)
        
        self.vbox.pack_start(alignment)
        self.window.add(self.vbox)
        self.window.show_all()
        
        self.window.connect("destroy", self.destroy_handler)
        self.not_destroyed = True
        
    def destroy_handler(self, widget):
        self.not_destroyed = False
        
    def ok_clicked(self, widget):
        self.window.hide()
        
    def revert_all(self, widget):
        self.plot.apply_config(self.revert_data, None)
        for option_name in self.options:
            if (self.options[option_name].configurable):
                self.set_val(option_name, self.revert_data)
        
    def show_color_selection_dialog(self, widget, dialog):
        response = dialog.run()
        if (response != Gtk.ResponseType.OK):
            color_selection = dialog.get_color_selection()
            color_selection.set_current_color(color_selection.get_previous_color())
        dialog.hide()
    
    def apply_all(self, widget):
        self.plot.apply_config(None, self.get_val)
            
    def set_val(self, option_name, revert_data):
        data_type = self.options[option_name].data_type
        revert_val = revert_data[option_name]
        if (data_type == 'text'):
            self.controls[option_name].set_text(revert_val)
        elif (data_type == 'combo'):
            revert_val_index = self.options[option_name].combo.index(revert_val)
            self.controls[option_name].set_active(revert_val_index)
        elif (data_type == 'boolean'):
            self.controls[option_name].set_active(revert_val)
        elif (data_type == 'slider'):
            self.controls[option_name].set_value(revert_val)

        self.controls[option_name].queue_draw()
        
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
        elif (data_type == 'combo'):
            text = self.controls[option_name].get_active_text()
            self.controls[option_name].queue_draw()
            return text
        elif (data_type == 'boolean'):
            return self.controls[option_name].get_active()
        elif (data_type == 'color'):
            rgba = self.controls[option_name].get_current_color()
            return (rgba.red/65535.0, rgba.green/65535.0, rgba.blue/65535.0)
        elif (data_type == 'slider'):
            return self.controls[option_name].get_value()
