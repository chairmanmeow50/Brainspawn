import numpy as np
import matplotlib.pyplot as plt
import __future__


class Spike_Raster_Plot():
    '''Generate a raster plot of the provided spike data

    Parameters
    ----------
    time : array
        Time data from the simulation
    spikes: array
        The spike data with columns for each neuron and 1s indicating spikes
    ax: matplotlib.axes.Axes
        The figure axes to plot into.

    Returns
    -------
    ax: matplotlib.axes.Axes
        The axes that were plotted into

    Examples
    --------
    >>> import nengo
    >>> model = nengo.Model("Raster")
    >>> A = nengo.Ensemble(nengo.LIF(20), dimensions=1)
    >>> A_spikes = nengo.Probe(A, "spikes")
    >>> sim = nengo.Simulator(model)
    >>> sim.run(1)
    >>> rasterplot(sim.trange(), sim.data(A_spikes))
    '''
    '''
    def __init__(self, simulator, name, func, args=(), label=None, Fs=1.0):
        self.plot_name = "spike raster" + name
        self.simulator = simulator
        self.func = func
        self.data = self.simulator.watcher_manager.activate_watcher(name,
                func, args=args)
        self.fig = plt.figure(self.plot_name)
        self.fig.patch.set_facecolor('white')
        self.ax = plt.subplot(111)
        self.Fs = Fs
        
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.title('LFP Spectrogram')
        '''
    
    def get_figure(self):
        return self.figure
        
    def tick(self):
        
        '''
        spikes = [time[spikes[:, i] > 0].flatten()
          for i in range(spikes.shape[1])]
        for ix in range(len(spikes)):
            if spikes[ix].shape == (0,):
        spikes[ix] = np.array([-1])
        '''
        spikes = []
        
        start = self.simulator.min_tick
        count = self.simulator.current_tick - self.simulator.min_tick
        data = self.data.get(start, count) # the signal
        print data
        #print data
        
        #for i in range(spikes.shape[1]):
        #    self.ax.plot(data[spikes[:, i] > 0],
        #            np.ones_like(np.where(spikes[:, i] > 0)).T + i, ',',
        #            None)
        

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
        
        #self.draw_rects()
        plt.title('Raster Spike Plot')
        
        #if self.ax is None:
        self.ax = plt.gca()
    
        #colors = kwargs.pop('colors', None)
        #if colors is None:
        #    color_cycle = plt.rcParams['axes.color_cycle']
        #    colors = [color_cycle[ix % len(color_cycle)]
        #              for ix in range(spikes.shape[1])]
    
    '''
        if hasattr(ax, 'eventplot'):
            spikes = [time[spikes[:, i] > 0].flatten()
                      for i in range(spikes.shape[1])]
            for ix in range(len(spikes)):
                if spikes[ix].shape == (0,):
                    spikes[ix] = np.array([-1])
            ax.eventplot(spikes, colors=colors, **kwargs)
            ax.set_ylim(len(spikes) - 0.5, -0.5)
            if len(spikes) == 1:
                ax.set_ylim(0.4, 1.6)  # eventplot plots different for len==1
            ax.set_xlim(left=0)
            '''
    '''
        else:
            # Older Matplotlib, doesn't have eventplot
            for i in range(spikes.shape[1]):
                ax.plot(time[spikes[:, i] > 0],
                        np.ones_like(np.where(spikes[:, i] > 0)).T + i, ',',
                        color=colors[i], **kwargs)
                        '''
    