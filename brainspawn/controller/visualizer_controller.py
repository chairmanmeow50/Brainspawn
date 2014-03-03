#
"""
Main Controller for the app
"""

import glob
import os
import imp
import traceback

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

        self.main_frame = MainFrame(self.sim_manager)
        self.load_visualization_files()

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
                    self.main_frame.add_plot(plot_obj)
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

