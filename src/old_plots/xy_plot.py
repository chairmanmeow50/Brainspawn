import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pylab import *

class XY_Plot():
    
    def tick(self):
        #self.i += 1
        #self.t = arange(0+self.i, 10+self.i, 0.01)
        start = self.simulator.min_tick
        count = self.simulator.current_tick - self.simulator.min_tick
        data = self.data.get(start, count) # the signal
        
        t = np.linspace(start, start +
                data.size * self.simulator.dt, data.size)
        self.l.set_xdata(t)
        self.s = data
        self.l.set_ydata(self.s)
        
    def get_figure(self):
        return self.figure
    
    def clear(self):
        self.s = np.empty(self.t.size)
        self.l.set_ydata(self.s)

    def __init__(self, simulator, name, func, args=(), label=None, Fs=1.0):
        #self.i = 0
        self.simulator = simulator
        self.figure = plt.figure()
        self.figure.patch.set_facecolor('white')
        
        self.data = self.simulator.watcher_manager.activate_watcher(name,
                func, args=args)
        
        start = self.simulator.min_tick
        count = self.simulator.current_tick - self.simulator.min_tick
        data = self.data.get(start, count) # the signal

        self.t = np.linspace(start, start +
                data.size * self.simulator.dt, data.size)
#         self.t = arange(0.0, 10, 0.01)
#         self.s = np.random.rand(self.t.size)
        self.l, = plt.plot(self.t, data, 'r-')
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

    
