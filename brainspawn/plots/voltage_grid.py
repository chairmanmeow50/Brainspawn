""" Module for voltage grid. Ported from Java nengo. Currently not enabled
because getting voltage data from a voltage capability is not working.
"""

import numpy as np
from matplotlib.patches import Rectangle
from plots.plot import Plot
from plots.base_plot import registered_plot
from plots.firing_rate import Firing_Rate_Plot
import __future__
import random


@registered_plot
class Voltage_Grid_Plot(Firing_Rate_Plot):
    """ Class for voltage grid plot. Extends from a firing rate plot.
    """

    @staticmethod
    def plot_name():
        """ Returns name of plot.
        """
        return "Voltage Grid Plot"

    @staticmethod
    def supports_cap(cap):
        """ Returns whether or not this plot supports the given capability.
        """
        return cap.name in ['voltage']

    def update(self, start_step, step_size, data):
        """ Sets a random color for each rectangle square.

        TODO: When voltage capability is working, the correct color should
        reflect the voltage value of the neuron.
        """

        for i in xrange(0, self.rows, 1):
            for j in xrange(0, self.rows, 1):
                random_val = random.random()
                self.rect_array[i][j].set_facecolor(
                    self.voltage_color(random_val))

    def voltage_color(self, voltage):
        """ Converts the voltage value to a distribution of colours between
        yellow and white to black. The distribution is arbitrary right now.

        TODO: When voltages is working, should fix the distribution to be
        actually meaningful."""
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

    def draw_rects(self):
        """ Draws the initial rectangles.
        """
        width = 1.0 / self.rows
        height = 1.0 / self.rows

        for x in xrange(0, self.rows, 1):
            for y in xrange(0, self.rows, 1):
                rect = Rectangle((x/float(self.rows), y/float(self.rows)),
                                 width, height, facecolor="#000000")
                self.rect_array[x].append(rect)
                self.axes.add_patch(rect)

    def __init__(self, main_controller, obj, cap, config=None):
        """ Calls parent constructor.
        """
        super(Voltage_Grid_Plot, self).__init__(main_controller, obj, cap,
                                                config)
        self.axes = self.figure.add_subplot(111)
        self.axes.patch.set_alpha(0.0)
        self.axes.set_title(self.title)
