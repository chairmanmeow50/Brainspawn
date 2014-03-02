#
"""
Main Controller for the app
"""

# use this for now
import brainspawn.sample_networks.two_dimensional_rep as example
from brainspawn.simulator.sim_manager import SimManager
from brainspawn.view.visualizer import MainFrame

class VisualizerController(object):
    """
    A controller
    """

    def __init__(self):
        self.sim_manager = SimManager()
        self.dt = 0.001

        self.plots = []

        # TODO - Hardcoding model for now
        # At some point, we'll add a file -> open menu
        self.load_model(example.model)

        self.main_frame = MainFrame(self)

    def init_view(self):
        pass

    def load_model(self, model):
        self.model = model
        self.sim_manager.load_new_model(model, self.dt) # do we want to copy the model?

    def add_plot(self, plot):
        """ COMPLETELY PLACEHOLDER AT THE MOMENT
        """
        node_caps = self.sim_manager.get_caps_for_obj(example.neurons)
        for cap in node_caps:
            print (cap.name, cap.get_out_dimensions(example.neurons))
            if (cap.name is 'output'):
                out_cap = cap

        self.sim_manager.connect_to_obj(example.neurons, out_cap, plot.update)
