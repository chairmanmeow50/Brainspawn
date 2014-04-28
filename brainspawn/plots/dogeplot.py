""" Visualization demonstrating extending an existing plot class and adding
additional functionality on top.
"""


from plots.value_plot import ValuePlot
from plots.base_plot import registered_plot


@registered_plot
class DogePlot(ValuePlot):
    """ DogePlot class. Same as ValuePlot except for some text drawn on top.
    """

    def __init__(self, main_controller, obj, cap):
        """ Initializes plot by calling parent constructor.
        Adds text onto plot axes.
        """
        super(DogePlot, self).__init__(main_controller, obj, cap)
        self.text = []
        self.text.append(self.axes.text(0.27, 0.77, "such line", fontsize=12,
                                        color='orange'))
        self.text.append(self.axes.text(0.7, 0.57, "very neuron", fontsize=12,
                                        color='green'))
        self.text.append(self.axes.text(0.77, 0.2, "wow", fontsize=12,
                                        color='purple'))
        self.text.append(self.axes.text(0.07, 0.32, "so science", fontsize=12,
                                        color='cyan'))

    @staticmethod
    def plot_name():
        """ Return name of plot.
        """
        return "Doge"

    def update(self, start_step, step_size, data):
        """ Calls parent update function.
        Moves all text's x coordinate based on simulation time step.
        """
        super(DogePlot, self).update(start_step, step_size, data)
        if (self.text and len(data) < 275):
            for txt in self.text:
                txt.set_x((txt.get_position()[0]*100000+len(data))/100000 % 1)
