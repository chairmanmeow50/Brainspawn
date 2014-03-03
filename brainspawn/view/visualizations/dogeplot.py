import numpy as np
import matplotlib.pyplot as plt
from view.visualizations.xy_plot import XYPlot

def class_name():
    return "DogePlot"

class DogePlot(XYPlot):
    """DogePlot
    """

    def name(self):
        return "Doge Plot"

    def __init__(self, sim_manager, main_controller, **kwargs):
        super(DogePlot, self).__init__(sim_manager, main_controller, **kwargs)
        self.text = []
        self.text.append(plt.text(0.27, 0.77, "such line", fontsize=12, color='orange'))
        self.text.append(plt.text(0.7, 0.57, "very neuron", fontsize=12, color='green'))
        self.text.append(plt.text(0.77, 0.2, "wow", fontsize=12, color='purple'))
        self.text.append(plt.text(0.07, 0.32, "so science", fontsize=12, color='cyan'))

    @staticmethod
    def display_name(cap):
        return "so science" + " " + cap.name


    def update(self, data, start_time):
        super(DogePlot, self).update(data, start_time)
        if (self.text and len(data) < 275):
            for txt in self.text:
                txt.set_x((txt.get_position()[0]*100000 + len(data))/100000 % 1 )

