import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pylab import *
import sys
from mpl_toolkits.axes_grid1 import AxesGrid

class Voltage_Grid_Plot():
    def update_line(self, num, data, line):
        print num
        line.set_data(data[...,:num])
        return line,
    
    def tick(self):
        width = 1 / 10.0
        height = 1 / 10.0
        for x in xrange(0, 10, 1):
            for y in xrange(0, 10, 1):
                self.rect_array[x][y].set_facecolor(self.random_color())
                #self.rect_array[x][y] = plt.Rectangle((x/10.0, y/10.0), width, height, facecolor=self.random_color())
        
    def get_figure(self):
        return self.figure

    def update_canvas():
        return
    
    def random_color(self):
        r = lambda: np.random.randint(0,255)
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
        #color = "#%02X%02X%02X".format(r(), r(), r())
        #color = "#%02X%02X%02X".format(100, 100, 200)
        color = np.random.rand(3, 1)
        #print color
        return set_of_colors[np.random.randint(0, 4)]
    
    def draw_rects(self):
        width = 1 / 10.0
        height = 1 / 10.0
        facecolor = "#aaaaaa"
        
        for x in xrange(0, 10, 1):
            for y in xrange(0, 10, 1):
                rect = plt.Rectangle((x/10.0, y/10.0), width, height, facecolor=self.random_color())
                self.rect_array[x].append(rect)
                plt.gca().add_patch(rect)
                
        
        

    def __init__(self):
        self.i = 0
        self.figure = plt.figure()
        
        self.rect_array = [[] for i in range(10)]
        print self.rect_array
        
        self.t = arange(0.0, 10, 0.01)
        #self.s = sin(2*pi*self.t)
        #self.data = np.random.rand(2, 25)
        #self.l, = plt.plot(self.t, [], 'r-')
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.xlabel('x')
        
        self.draw_rects()
        #plt.ion()
        plt.title('Voltage Grid Plot')
        #plt.show()
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

    
