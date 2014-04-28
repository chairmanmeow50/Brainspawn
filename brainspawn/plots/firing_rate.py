""" Firing rate visualization. Ported from the Java version of Nengo.
"""

import numpy as np
import math
from matplotlib.patches import Rectangle
from plots.plot import Plot
from plots.base_plot import registered_plot


@registered_plot
class Firing_Rate_Plot(Plot):
    """ Firing rate plot. Extends from the Plot class.
    """

    @staticmethod
    def plot_name():
        """ Returns name of plot.
        """
        return "Firing Rate"

    @staticmethod
    def supports_cap(cap):
        """ Supports 'spikes' capability.
        """
        return cap.name in ['spikes']

    def update(self, start_step, step_size, data):
        """ Paints a rectangle with a shade depending on its previous values.
        If it fired on this tick, it will be white. If it fired on the previous
        tick, it will be slightly grayer.
        """
        if (len(data) == 0):
            self.clear()
            return

        length = len(data[-1])
        row = int(math.floor(math.sqrt(length)))
        col = row
        for i in xrange(0, self.rows, 1):
            for j in xrange(0, self.rows, 1):
                if (data[-1][i*self.rows + j]):
                    self.rect_array_color[i][j] = 4
                elif (len(data) >= 2 and data[-2][i*self.rows + j]):
                    self.rect_array_color[i][j] = 3
                elif (len(data) >= 3 and data[-3][i*self.rows + j]):
                    self.rect_array_color[i][j] = 2
                elif (len(data) >= 4 and data[-4][i*self.rows + j]):
                    self.rect_array_color[i][j] = 1
                elif (len(data) >= 5 and data[-5][i*self.rows + j]):
                    self.rect_array_color[i][j] = 0

                color = self.get_color(self.rect_array_color[i][j])
                self.rect_array[i][j].set_facecolor(color)

    def get_color(self, color_value):
        """ Returns a colour based on a numeric value. Starting from 4, the
        colour is white, and as the value goes down, becomes closer to black.
        """
        if (color_value == 4):
            return "#FFFFFF"
        elif (color_value == 3):
            return "#BBBBBB"
        elif (color_value == 2):
            return "#777777"
        elif (color_value == 1):
            return "#333333"
        else:
            return "#000000"

    def clear(self):
        """ Sets all the grid rectangles to black.
        """
        for i in xrange(0, self.rows, 1):
            for j in xrange(0, self.rows, 1):
                self.rect_array[i][j].set_facecolor("#000000")

    def draw_rects(self):
        """ Draws and initializes the initial rectangles.
        """
        width = 1.0 / self.rows
        height = 1.0 / self.rows

        for x in xrange(0, self.rows, 1):
            for y in xrange(0, self.rows, 1):
                rect = Rectangle((x/float(self.rows), y/float(self.rows)),
                                 width, height, facecolor="#000000")
                self.rect_array[x].append(rect)
                self.rect_array_color[x] = np.zeros(self.rows)
                self.axes.add_patch(rect)

    def __init__(self, main_controller, obj, cap):
        """ Calls the parent constructor.
        Creates x number of rows, where x is the square root of number of
        dimensions (which means the number of neurons in an ensemble).
        """
        super(Firing_Rate_Plot, self).__init__(main_controller, obj, cap)

        self.axes = self.figure.add_subplot(111)  # take first from list
        self.axes.patch.set_alpha(0.0)
        self.axes.set_title(self.title)

        self.rows = int(math.floor(math.sqrt(self.dimensions)))

        self.rect_array = [[] for i in range(self.rows)]
        self.rect_array_color = [[] for i in range(self.rows)]
        self.axes.set_xlim(0, 1)
        self.axes.set_ylim(0, 1)
        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)

        self.draw_rects()
