#
"""
Main Controller for the app
"""

import os
import gtk
import cairo
from simulator.sim_manager import SimManager
from view.visualizer import MainFrame

# FIXME use this for now
import sample_networks.two_dimensional_rep as example

class VisualizerController(object):
    """
    A controller
    """

    def __init__(self):
        self.sim_manager = SimManager()
        self.dt = 0.001

        # TODO - Hardcoding model for now
        # At some point, we'll add a file -> open menu
        self.load_model(example.model)

        self.main_frame = MainFrame(self.sim_manager, self)

    def init_view(self):
        pass

    def load_model(self, model):
        self.model = model
        self.sim_manager.load_new_model(model, self.dt) # do we want to copy the model?

    def load_visualization_files(self):
        # find all files in view/visualizations ending in .py and doesn't start with __
        visualization_files = glob.glob('brainspawn/view/visualizations/*.py')
        for full_file_name in visualization_files:
            file_name = full_file_name[full_file_name.rfind('/')+1:]
            if (file_name.startswith("__") == False):
                plot_obj = self.load_from_file(full_file_name, self.sim_manager)
                self.register_visualization(plot_obj)
                if (plot_obj != None):
                    self.main_frame.controller.add_plot(plot_obj)
                    self.main_frame.all_plots.append(plot_obj)
                    self.main_frame.all_canvas.append(plot_obj.canvas)

    def register_visualization(self, visualization_object):
        if visualization_object != None:
            print visualization_object.name()

    def load_from_file(self, filepath, manager):
        class_inst = None
        expected_class = 'MyClass'

        mod_name,file_ext = os.path.splitext(os.path.split(filepath)[-1])

        if file_ext.lower() == '.py':
            py_mod = imp.load_source(mod_name, filepath)

        elif file_ext.lower() == '.pyc':
            py_mod = imp.load_compiled(mod_name, filepath)

        mod_class = getattr(py_mod, py_mod.class_name())
        try:
            class_inst = mod_class(manager)
        except TypeError as e:
            print "Error instantiating class " + py_mod.class_name()
            print traceback.print_exc()

        return class_inst

    def on_export_pdf(self, widget):
        filename = self.file_browse(gtk.FILE_CHOOSER_ACTION_SAVE, "screenshot.pdf")
        if not filename:
            return
        with open(filename, "wb") as f:
            cr = cairo.Context(cairo.PDFSurface(f, *self.main_frame.window.get_size()))
            rect = gtk.gdk.Rectangle()
            rect.x = rect.y = 0
            rect.width, rect.height = self.main_frame.window.get_size()
            self.main_frame.window.size_allocate(rect)
            self.main_frame.window.draw(cr)
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


