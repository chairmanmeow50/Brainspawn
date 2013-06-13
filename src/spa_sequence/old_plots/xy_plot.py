import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class XY_Plot():
    def update_line(self, num, data, line):
        line.set_data(data[...,:num])
        return line,

    def get_figure(self):
        return self.figure

    def update_canvas():
        return

    def __init__(self):
        self.figure = plt.figure()

        self.data = np.random.rand(2, 25)
        self.l, = plt.plot([], [], 'r-')
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.xlabel('x')
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

    
