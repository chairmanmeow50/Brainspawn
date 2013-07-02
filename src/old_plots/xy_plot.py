import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pylab import *

class XY_Plot():
    
    def tick(self):
        print "xy tick"
        #self.i += 1
        #self.t = arange(0+self.i, 10+self.i, 0.01)
        self.s = np.random.rand(self.t.size)
        self.l.set_ydata(self.s)
        
    def get_figure(self):
        return self.figure

    def __init__(self):
        #self.i = 0
        self.figure = plt.figure()

        self.t = arange(0.0, 10, 0.01)
        self.s = np.random.rand(self.t.size)
        self.l, = plt.plot(self.t, self.s, 'r-')
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.xlabel('x')
        plt.title('XY Plot')

if __name__ == "__main__":
    xy = XY_Plot()
    fig = xy.get_figure()
    fig.show()
    line_ani = animation.FuncAnimation(fig, xy.update_line, 25, fargs=(xy.data, xy.l),
    interval=50, blit=True)
    plt.show()

    
