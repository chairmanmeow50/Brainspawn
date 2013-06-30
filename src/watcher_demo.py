from spa_sequence.spa_sequence import net, pThal

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

import simulator
import simulator.watchers
import view.components


class WatcherDemo:

    def __init__(self):
        self.sim = simulator.Simulator(net, net.dt)
        self.sim.add_watcher(simulator.watchers.LFPSpectrogramWatcher())
        self.sim.watcher_manager.add_object("pThal", pThal)
        self.spectrogram = None

        net.run(0.001) #run for one timestep

    def display_spectrogram(self):
        # Say we're searching through the layout file
        #TODO - implement Layout files
        for name, type, data in [("pThal", "LFP Spectrogram", None)]:
            if name in self.sim.watcher_manager.objects.keys():
                for (t, view_class, args) in self.sim.watcher_manager.list_watcher_views(name):
                    if t == type:
                        component = view_class(self.sim, name, **args)
                        # we know we only have the spectrogram in our example
                        self.spectrogram = component

    def start_animate(self):
        # set the animation interval based on the time to animate one step
        t0 = time.time()
        self.animate(0)
        interval = max(0, 30 - 1000 * (time.time() - t0))
        self._ani = animation.FuncAnimation(self.spectrogram.fig, self.animate, interval=interval, blit=True)

    def animate(self, i):
        self.sim.tick()
        return self.spectrogram.tick()

if __name__ == "__main__":
    demo = WatcherDemo()
    demo.display_spectrogram()
    demo.start_animate()
    plt.show()
