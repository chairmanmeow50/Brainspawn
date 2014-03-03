import numpy as np
import matplotlib.pyplot as plt
from view.visualizations.__visualization import Visualization
from view.visualizations.firing_rate import Firing_Rate_Plot
import __future__
import random

def class_name():
    return "Voltage_Grid_Plot"

class Voltage_Grid_Plot(Firing_Rate_Plot):
    def out_cap(self):
        return "spikes"

    def display_name(self):
        return "Voltage Grid Plot"

    def supports_cap(self, cap, dimensions):
        return cap.name() in ['spikes']

    def update(self, data, start_time):
        """ after a tick, gets the values of the neurons and
        each row represents the value of the neurons
        the columns show the values over time
        """
        
        latest_data_i = len(data) - 1
        for i in xrange(0, self.rows, 1):
            for j in xrange(0, self.columns, 1):
                #srandom_val = 0
                #if (data[latest_data_i][j*self.rows + i]):
                random_val = random.random()
                self.rect_array[i][j].set_facecolor(self.voltage_color(random_val))

    def voltage_color(self, voltage):
        """ converts the voltage value to a
        distribution of colours between yellow
        and white to black"""
        set_of_colors = []
        # black
        set_of_colors.append('#000000')
        # grey 1
        set_of_colors.append('#474747')
        # grey 2
        set_of_colors.append('#B2B2B2')
        # white
        set_of_colors.append('#FFFFFF')
        # yellow
        set_of_colors.append('#FFFF66')

        if (voltage > 0.95):
            return set_of_colors[4]
        elif (voltage > 0.9):
            return set_of_colors[3]
        elif (voltage > 0.7):
            return set_of_colors[2]
        elif (voltage > 0.6):
            return set_of_colors[1]
        else:
            return set_of_colors[0]

    def random_color(self):
        set_of_colors = []
        # white
        set_of_colors.append('#000000')
        # grey 1
        set_of_colors.append('#B2B2B2')
        # grey 2
        set_of_colors.append('#474747')
        # yellow
        set_of_colors.append('#FFFF66')
        # black
        set_of_colors.append('#FFFFFF')
        #color = np.random.rand(3, 1)
        return set_of_colors[np.random.randint(0, 4)]

    def draw_rects(self):
        """ draws the initial rectangles"""
        width = 1.0 / self.rows
        height = 1.0 / self.columns

        for x in xrange(0, self.rows, 1):
            for y in xrange(0, self.columns, 1):
                rect = plt.Rectangle((x/float(self.rows), y/float(self.columns)), width, height, facecolor="#000000")
                self.rect_array[x].append(rect)
                plt.gca().add_patch(rect)

    def __init__(self, sim_manager, **kwargs):

        self.sim_manager  = sim_manager
        self._figure = plt.figure()
        self.init_canvas(self._figure)
        self._figure.patch.set_facecolor('white')

        self.rows = kwargs.get('rows') if 'rows' in kwargs else 10
        self.columns = kwargs.get('columns') if 'columns' in kwargs else 10

        self.rect_array = [[] for i in range(self.rows)]
        plt.xlim(0, 1)
        plt.ylim(0, 1)

        self.draw_rects()
        name = kwargs.get('name') if 'name' in kwargs else self.display_name()
        plt.title(name)
