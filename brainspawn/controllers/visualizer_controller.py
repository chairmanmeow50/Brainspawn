#
"""
Main controller for visualizer
"""

import os
import imp
import gtk
import cairo
import json
import traceback
import settings
from gi.repository import Gtk

from views.visualizer import MainFrame
from views.network_view import NetworkView
from plots.base_plot import REGISTERED_PLOTS

class VisualizerController(object):
    """
    A controller
    """

    def __init__(self, sim_manager, model_file_name=None):
        self.sim_manager = sim_manager
        self.network_view = NetworkView(self)
        self.dt = settings.SIMULATOR_DEFAULT_DELTA_TIME

        self.registered = []
        self.plots = []
        self.load_plots()

        self._has_network = False
        self._loaded_model_file = None

        # instantiates main visualizer frame
        self.main_frame = MainFrame(self.sim_manager, self)

        if (model_file_name):
            self.load_model_from_filename(model_file_name, load_layout=True)

    def plots_for_object(self, obj):
        """ Returns a list of plots available for this object
        """
        supported_plots = []
        node_caps = self.sim_manager.get_caps_for_obj(obj)
        for cap in node_caps:
            for vz in self.registered:
                if vz.supports_cap(cap):
                    supported_plots.append((vz, obj, cap))
        return supported_plots

    def add_plot_for_obj(self, plt, obj, cap, config=None, position=None, 
                         size=None):
        """ Callback for menu item
        """
        plot = plt(self, obj, cap)
        plot.set_config_values(config)
        self.plots.append(plot)
        self.sim_manager.connect_to_obj(obj, cap, plot.update)
        self.main_frame.show_plot(plot, False, position, size)

    def remove_plot_for_obj(self, plot, obj, cap):
        self.sim_manager.disconnect_from_obj(obj, cap, plot.update)
        self.plots.remove(plot)
        self.main_frame.remove_plot(plot)

    def on_quit(self):
        if self._loaded_model_file:
            filename = os.path.splitext(self._loaded_model_file)[0] + \
                settings.LAYOUT_FILE_EXTENSION
            with open(filename, 'wb') as f:
                json.dump(self.get_layout_dict(), f)

    def on_open_model(self, widget):
        filename = self.file_open(ext=settings.PYTHON_FILE_EXTENSION, 
                                  ext_name=settings.PYTHON_FILE_EXTENSION_NAME)
        if not filename:
            return
        self.load_model_from_filename(filename, load_layout=True)

    def restore_layout_dict(self, dct, load_model=False):
        """Restores layout from dict
        Throws:
            ValueError - dct could not be loaded
        """
        layout_dict = dct['layout']

        # Restore model file
        if load_model:
            self.load_model_from_filename(layout_dict['model'], 
                                          load_layout=False)

        # Restore plots
        for plot_dict in layout_dict['plots']:
            target_obj = self.get_nengo_for_uid(plot_dict['target_obj'])
            target_cap_name = plot_dict['target_cap']
            target_cap = None
            for cap in self.sim_manager.get_caps_for_obj(target_obj):
                if cap.name == target_cap_name:
                    target_cap = cap
            if not target_cap:
                raise ValueError("No capability for nengo object: " + \
                                 target_obj + " with name: " + target_cap_name)
            plot_type = plot_dict['plot_type']
            for plot_cls in self.registered:
                if plot_type == plot_cls.__name__:
                    self.add_plot_for_obj(plot_cls, target_obj, 
                                          target_cap, plot_dict['config'], 
                                          plot_dict['position'], 
                                          plot_dict['size'])
                    break
            else:
                # loop exited without break
                raise ValueError("No plot:" + plot_type + "for nengo object: " \
                                 + target_obj + " with name: " + \
                                 target_cap_name)

        # Restore network
        net_dict = layout_dict['network']
        self.main_frame.set_item_position(self.network_view, 
                                          net_dict['position'])
        self.main_frame.set_item_size(self.network_view, net_dict['size'])
        self.network_view.restore_layout(net_dict['network_layout'])

    def get_layout_dict(self):
        layout_dict = {}
        # Save model file
        layout_dict['model'] = self._loaded_model_file
        # Save plots
        layout_dict['plots'] = []
        for plot in self.plots:
            plot_dict = {}
            plot_dict['plot_type'] = plot.__class__.__name__
            plot_dict['target_obj'] = self.get_uid_for_nengo(plot.nengo_obj)
            plot_dict['target_cap'] = plot.capability.name
            plot_dict['position'] = self.main_frame.get_item_position(plot)
            plot_dict['size'] = self.main_frame.get_item_size(plot)
            plot_dict['config'] = plot.get_config_values()
            layout_dict['plots'].append(plot_dict)
        # Save network
        net_dict = {}
        net_dict['position'] = \
            self.main_frame.get_item_position(self.network_view)
        net_dict['size'] = self.main_frame.get_item_size(self.network_view)
        net_dict['network_layout'] = self.network_view.store_layout()
        layout_dict['network'] = net_dict
        return {'layout': layout_dict}

    def get_uid_for_nengo(self, nengo_obj):
        """Gets a consistent uid for the given nengo object
        """
        # Let's just use the network view's method right now, 
        # since that seems to be working great
        return self.network_view.get_name_from_obj(nengo_obj)

    def get_nengo_for_uid(self, uid):
        """Gets a nengo object for a given uid
        """
        return self.network_view.get_obj_from_name(uid)

    def load_model_from_filename(self, filename, load_layout=False):
        mod_name, file_ext = os.path.splitext(os.path.basename(filename))
        try:
            module = imp.load_source(mod_name, filename)
            self.load_model(module.model)
            self._loaded_model_file = filename
            if (not self._has_network):
                self.main_frame.show_plot(self.network_view, True)
                self._has_network = True
                self.main_frame.controller_panel.enable_controls()
        except (AttributeError, ImportError, IOError, SyntaxError) as e:
            print e
            self.show_err_dialog("Error loading model", 
                                 "Could not load model from " + str(filename))

        if load_layout:
            try:
                layout_file = \
                    os.path.splitext(self._loaded_model_file)[0] + '.bpwn'
                if not layout_file:
                    return
                with open(layout_file, 'rb') as f:
                    self.restore_layout_dict(json.load(f))
            except Exception as e:
                # If the layout file isn't there, don't bug user...
                if type(e) is not IOError:
                    traceback.print_exc()
                    self.show_err_dialog("Error loading layout for model", 
                                         "Could not load layout from " + \
                                         str(layout_file))
                    self.load_model_from_filename(filename, load_layout=False)
                    self.network_view.init_default_config()

    def show_err_dialog(self, message, secondary):
        dialog = Gtk.MessageDialog(self.main_frame.window, 0, 
                                   Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK, message)
        dialog.format_secondary_text(secondary)
        dialog.run()
        dialog.destroy()


    def load_model(self, model):
        copy_plots = self.plots[:]
        for plt in copy_plots:
            plt.remove_plot(None, None)
        self.plots = []
        if self.sim_manager.current_step > 0:
            self.main_frame.reset_button(None) # a little hacky, but hey
        self.model = model
        self.main_frame.window.set_title("Nengo Visualizer - " + model.label)
        self.network_view.load_model(model)
        self.sim_manager.load_new_model(model, self.dt) 

    def load_plots(self):
        plots_dir = os.path.join(os.path.dirname(__file__), "../plots/")
        for name in os.listdir(plots_dir):
            if name.endswith(".py") and not name.startswith("_"):
                self.load_module(os.path.join(plots_dir, name))
        self.registered = REGISTERED_PLOTS.values()

    def load_module(self, filename):
        mod_name, ext = os.path.splitext(os.path.basename(filename))
        return imp.load_source(mod_name, filename)

    def on_layout_button_release(self, widget, event):
        if event.button == 3:
            export_pdf_item = gtk.MenuItem("Export to PDF...")
            export_pdf_item.connect("activate", self.on_export_pdf, widget)
            export_pdf_item.show()
            self.layout_context_menu = gtk.Menu()
            self.layout_context_menu.append(export_pdf_item)
            self.layout_context_menu.popup(None, None, None, None, 
                                           event.button, event.time)
            return True
        return False

    def on_export_pdf(self, event_widget, widget, name=None):
        if not name:
            name = self.main_frame.window.get_title()
        filename = self.file_save(name + ".pdf")
        if not filename:
            return
        with open(filename, "wb") as f:
            allocation = widget.get_allocation()
            cr = cairo.Context(cairo.PDFSurface(f, allocation.width, 
                                                allocation.height))
            try:
                widget.on_draw_event(None, cr)
            except AttributeError:
                widget.draw(cr)
            cr.show_page()
            cr.get_target().finish()

    def file_open(self, ext="", ext_name=""):
        buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
                   gtk.STOCK_OPEN, gtk.RESPONSE_OK)
        return self._file_browse(gtk.FILE_CHOOSER_ACTION_OPEN, 
                                 buttons, "", ext, ext_name)

    def file_save(self, name="", ext="", ext_name=""):
        buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
                   gtk.STOCK_SAVE, gtk.RESPONSE_OK)
        return self._file_browse(gtk.FILE_CHOOSER_ACTION_SAVE, 
                                 buttons, name, ext, ext_name)

    def _file_browse(self, action, buttons, name="", ext="", ext_name=""):
        dialog = gtk.FileChooserDialog(title="Select File", 
                                       action=action, buttons=buttons)
        dialog.set_current_folder(os.getcwd())
        dialog.set_do_overwrite_confirmation(True)
        if action == gtk.FILE_CHOOSER_ACTION_SAVE:
            dialog.set_current_name(name)

        if ext:
            filt = gtk.FileFilter()
            filt.set_name(ext_name if ext_name else ext)
            filt.add_pattern("*." + ext)
            dialog.add_filter(filt)

        filt = gtk.FileFilter()
        filt.set_name("All files")
        filt.add_pattern("*")
        dialog.add_filter(filt)

        result = ""
        if dialog.run() == gtk.RESPONSE_OK:
            result = dialog.get_filename()
        dialog.destroy()
        return result
