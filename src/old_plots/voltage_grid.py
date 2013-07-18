import numpy as np
import matplotlib.pyplot as plt

class Voltage_Grid_Plot():
    def tick(self):
        for x in xrange(0, 10, 1):
            for y in xrange(0, 10, 1):
                self.rect_array[x][y].set_facecolor(self.random_color())
               
    def get_figure(self):
        return self.figure
    
    def clear(self):
        print "Not implemented yet"
    
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
        width = 1 / 10.0
        height = 1 / 10.0
        
        for x in xrange(0, 10, 1):
            for y in xrange(0, 10, 1):
                rect = plt.Rectangle((x/10.0, y/10.0), width, height, facecolor=self.random_color())
                self.rect_array[x].append(rect)
                plt.gca().add_patch(rect)
                
    def __init__(self):
        self.figure = plt.figure()
        
        self.rect_array = [[] for i in range(10)]
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        
        self.draw_rects()
        plt.title('Voltage Grid Plot')


    
