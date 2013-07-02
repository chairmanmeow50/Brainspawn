import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pylab import *
import sys

class XY_Plot():
    def update_line(self, num, data, line):
        print num
        line.set_data(data[...,:num])
        return line,
    
    def tick(self):
        print "xy tick"
        self.i += 1
        self.t = arange(0+self.i, 10+self.i, 0.01)
        self.s = np.random.rand(self.t.size)
        #sin(2*pi*self.t)
        #self.l.set_xdata(self.t)
        self.l.set_ydata(self.s)
        
    def get_figure(self):
        return self.figure

    def update_canvas():
        return

    def __init__(self):
        self.i = 0
        self.figure = plt.figure()

        self.t = arange(0.0, 10, 0.01)
        self.s = np.random.rand(self.t.size)
        #sin(2*pi*self.t)
        #self.data = np.random.rand(2, 25)
        self.l, = plt.plot(self.t, self.s, 'r-')
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.xlabel('x')
        #plt.ion()
        plt.title('XY Plot')
#line_ani.save('lines.mp4')

#fig2 = plt.figure()

#x = np.arange(-9, 10)
#y = np.arange(-9, 10).reshape(-1, 1)
#base = np.hypot(x, y)
#ims = []
#for add in np.arange(15):
#ims.append((plt.pcolor(x, y, base + add, norm=plt.Normalize(0, 30)),))

#im_ani = animation.ArtistAnimation(fig2, ims, interval=50, repeat_delay=3000,
#blit=True)
#im_ani.save('im.mp4', metadata={'artist':'Guido'})

#plt.show()


if __name__ == "__main__":
    xy = XY_Plot()
    fig = xy.get_figure()
    fig.show()
    line_ani = animation.FuncAnimation(fig, xy.update_line, 25, fargs=(xy.data, xy.l),
    interval=50, blit=True)
    plt.show()

    
