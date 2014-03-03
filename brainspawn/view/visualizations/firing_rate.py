import numpy as np
import matplotlib.pyplot as plt
from view.visualizations.__visualization import Visualization

import __future__

def class_name():
    return "Firing_Rate_Plot"

class Firing_Rate_Plot(Visualization):
    def out_cap(self):
        return "spikes"

    def display_name(self):
        return "Firing Rate Plot"

    def supports_cap(self, cap, dimensions):
        return cap.name() in ['spikes']
    
    def update(self, data, start_time):
        """ 
        paints a rectangle with a shade depending on 
        its previous values. if it fired on this tick
        it will be white, if it fired in the previous
        tick, it will be slightly grayer
        """
        
        latest_data_i = len(data) - 1
        for i in xrange(0, self.rows, 1):
            for j in xrange(0, self.columns, 1):
                if (data[latest_data_i][j*self.rows + i]):
                    self.rect_array_color[i][j] = 4
                else:
                    if (self.rect_array_color[i][j] >= 1):
                        self.rect_array_color[i][j] -= 1
                
                color = self.get_color(self.rect_array_color[i][j])
                self.rect_array[i][j].set_facecolor(color)

    def get_color(self, color_value):
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
        """ sets all the grids to black """
        for i in xrange(0, self.rows, 1):
            for j in xrange(0, self.columns, 1):
                self.rect_array[i][j].set_facecolor("#000000")
        
    def draw_rects(self):
        """ draws and initializes the initial rectangles """
        width = 1.0 / self.rows
        height = 1.0 / self.columns

        for x in xrange(0, self.rows, 1):
            for y in xrange(0, self.columns, 1):
                rect = plt.Rectangle((x/float(self.rows), y/float(self.columns)), width, height, facecolor="#000000")
                self.rect_array[x].append(rect)
                self.rect_array_color[x] = np.zeros(self.columns)
                plt.gca().add_patch(rect)

    def __init__(self, sim_manager, **kwargs):
        self.sim_manager  = sim_manager
        self._figure = plt.figure()
        self.init_canvas(self._figure)
        self._figure.patch.set_facecolor('white')

        self.rows = kwargs.get('rows') if 'rows' in kwargs else 10
        self.columns = kwargs.get('columns') if 'columns' in kwargs else 10

        self.rect_array = [[] for i in range(self.rows)]
        self.rect_array_color = [[] for i in range(self.rows)]
        plt.xlim(0, 1)
        plt.ylim(0, 1)

        self.draw_rects()
        name = kwargs.get('name') if 'name' in kwargs else self.display_name()
        plt.title(name)
