import numpy as np
import matplotlib.pyplot as plt
import __future__

class Voltage_Grid_Plot():
    def tick(self):
        start = self.simulator.min_tick
        count = self.simulator.current_tick - self.simulator.min_tick
        data = self.data.get(start, count) # the signal
        
        if (len(data) > 0):
            if (len(data[0]) == self.dimension):
                for i in xrange(0, self.dimension, 1):
                    for j in xrange(0, self.dimension, 1):
                        if (i < len(data) - 1):
                            x = len(data) - i - 1
                            # row should be == data len - 1
                            # column should be == 
#                             print "shape: " + str(data.shape)
                            voltage = data[x][j]
                            self.rect_array[i][j].set_facecolor(self.voltage_color(voltage))
        else:
            self.clear()
               
    def get_figure(self):
        return self.figure
    
    def clear(self):
        for i in xrange(0, self.dimension, 1):
            for j in xrange(0, self.dimension, 1):
                self.rect_array[i][j].set_facecolor("#000000")
        
    def voltage_color(self, voltage):
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
        
        if (voltage > 0.8):
            return set_of_colors[4]
        elif (voltage > 0.6):
            return set_of_colors[3]
        elif (voltage > 0.4):
            return set_of_colors[2]
        elif (voltage > 0.2):
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
        width = 1.0 / self.dimension
        height = 1.0 / self.dimension
        
        print "width: " + str(width)
        for x in xrange(0, self.dimension, 1):
            for y in xrange(0, self.dimension, 1):
                rect = plt.Rectangle((x/float(self.dimension), y/float(self.dimension)), width, height, facecolor="#000000")
                self.rect_array[x].append(rect)
                plt.gca().add_patch(rect)
                
    def __init__(self, simulator, name, func, args=(), label=None, Fs=1.0):
        self.simulator = simulator
        
        self.data = self.simulator.watcher_manager.activate_watcher(name,
                func, args=args)
        
        start = self.simulator.min_tick
        count = self.simulator.current_tick - self.simulator.min_tick
        data = self.data.get(start, count) # the signal
        
        self.dimension = len(data[0])
#         print "dimension:" + str(self.dimension)
        
        self.figure = plt.figure()
        self.figure.patch.set_facecolor('white')
        
        self.rect_array = [[] for i in range(self.dimension)]
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        
        self.draw_rects()
        plt.title('Voltage Grid Plot')


    
