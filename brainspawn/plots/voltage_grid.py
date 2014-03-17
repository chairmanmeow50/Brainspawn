import numpy as np
from matplotlib.patches import Rectangle
from plots.plot import Plot, registered_plot
from plots.firing_rate import Firing_Rate_Plot
import __future__
import random

@registered_plot
class Voltage_Grid_Plot(Firing_Rate_Plot):

    @staticmethod
    def plot_name():
        return "Voltage Grid Plot"

    @staticmethod
    def supports_cap(cap):
        return cap.name in ['voltage']

    def update(self, start_step, step_size, data):
        """ after a tick, gets the values of the neurons and
        each row represents the value of the neurons
        the columns show the values over time
        """

        # TODO - when voltages is fixed, implement
        for i in xrange(0, self.rows, 1):
            for j in xrange(0, self.rows, 1):
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
        height = 1.0 / self.rows

        for x in xrange(0, self.rows, 1):
            for y in xrange(0, self.rows, 1):
                rect = Rectangle((x/float(self.rows), y/float(self.rows)), width, height, facecolor="#000000")
                self.rect_array[x].append(rect)
                self.axes.add_patch(rect)

    def __init__(self, main_controller, obj, cap, config=None):
        super(Voltage_Grid_Plot, self).__init__(main_controller, obj, cap, config)
        self.axes = self.figure.add_subplot(111) # take first from list
        self.axes.patch.set_alpha(0.0)
        self.axes.set_title(self.title)

