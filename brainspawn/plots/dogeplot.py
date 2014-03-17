import numpy as np
from plots.value_plot import ValuePlot
from plots.base_plot import registered_plot

@registered_plot
class DogePlot(ValuePlot):
    """DogePlot
    """

    def name(self):
        return "Doge Plot"

    def __init__(self, main_controller, obj, cap):
        super(DogePlot, self).__init__(main_controller, obj, cap)
        self.text = []
        self.text.append(self.axes.text(0.27, 0.77, "such line", fontsize=12, color='orange'))
        self.text.append(self.axes.text(0.7, 0.57, "very neuron", fontsize=12, color='green'))
        self.text.append(self.axes.text(0.77, 0.2, "wow", fontsize=12, color='purple'))
        self.text.append(self.axes.text(0.07, 0.32, "so science", fontsize=12, color='cyan'))

    @staticmethod
    def plot_name():
        return "so science"


    def update(self, start_step, step_size, data):
        super(DogePlot, self).update(start_step, step_size, data)
        if (self.text and len(data) < 275):
            for txt in self.text:
                txt.set_x((txt.get_position()[0]*100000 + len(data))/100000 % 1 )

