#
"""
Main Controller for the app
"""

import glob
import os
import imp
import traceback
import gtk
import cairo

from simulator.sim_manager import SimManager
from view.visualizer import MainFrame
from view.visualizations._network_view import NetworkView

# FIXME use this for now
import sample_networks.two_dimensional_rep as example

class VisualizerController(object):
    """
    A controller
    """

    def __init__(self, sim_manager):
        self.sim_manager = sim_manager
        self.network_view = NetworkView(sim_manager, self)
        self.dt = 0.001

        self.registered = []
        self.plots = []

        # TODO - Hardcoding model for now
        # At some point, we'll add a file -> open menu
        self.load_model(example.model)

        self.main_frame = MainFrame(self.sim_manager, self)
        self.load_visualization_files()
        self.main_frame.show_plot(self.network_view)

    def init_view(self):
        pass

    def load_model(self, model):
        self.model = model
        self.network_view.load_model(model)
        self.sim_manager.load_new_model(model, self.dt) # do we want to copy the model?

    def load_visualization_files(self):
        # find all files in view/visualizations ending in .py and doesn't start with __
        visualization_files = glob.glob('brainspawn/view/visualizations/*.py')
        for full_file_name in visualization_files:
            file_name = full_file_name[full_file_name.rfind('/')+1:]
            if (file_name.startswith("_") == False):
                plot_cls = self.load_class_from_file(full_file_name)
                if plot_cls:
                    self.register_visualization(plot_cls)

    def register_visualization(self, visualization):
        self.registered.append(visualization)

    def load_class_from_file(self, filepath):
        """ Loads class from file as specified by module.class_name()
        """
        class_inst = None
        expected_class = 'MyClass'

        mod_name,file_ext = os.path.splitext(os.path.split(filepath)[-1])

        if file_ext.lower() == '.py':
            py_mod = imp.load_source(mod_name, filepath)

        elif file_ext.lower() == '.pyc':
            py_mod = imp.load_compiled(mod_name, filepath)

        mod_class = getattr(py_mod, py_mod.class_name())
        try:
            class_inst = mod_class(self.sim_manager, self)
        except TypeError as e:
            print "Error instantiating class " + py_mod.class_name()
            print traceback.print_exc()

        return mod_class

    def on_layout_button_release(self, widget, event):
        if event.button == 3:
            export_pdf_item = gtk.MenuItem("Export to PDF")
            export_pdf_item.connect("activate", self.on_export_pdf, widget)
            export_pdf_item.show()
            self.layout_context_menu = gtk.Menu()
            self.layout_context_menu.append(export_pdf_item)
            self.layout_context_menu.popup(None, None, None, None, event.button, event.time)
            return True
        return False

    def on_export_pdf(self, event_widget, widget):
        filename = self.file_browse(gtk.FILE_CHOOSER_ACTION_SAVE, "screenshot.pdf")
        if not filename:
            return
        with open(filename, "wb") as f:
            allocation = widget.get_allocation()
            cr = cairo.Context(cairo.PDFSurface(f, allocation.width, allocation.height))
            widget.draw(cr)
            cr.show_page()
            cr.get_target().finish()

    def file_browse(self, action, name="", ext="", ext_name=""):
        if (action == gtk.FILE_CHOOSER_ACTION_OPEN):
            buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK)
        else:
            buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK)
        dialog = gtk.FileChooserDialog(title="Select File", action=action, buttons=buttons)
        dialog.set_do_overwrite_confirmation(True)
        dialog.set_current_folder(os.getcwd())
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


