#!/usr/bin/env python
from pylab import *
from neo import io
from matplotlib import animation

hdf5file = io.NeoHdf5IO( filename = "spa_sequence/sequence.hd5" )

block = hdf5file.read_block()

# get analog signals
asig = block.segments[0].analogsignals[0]

dt = asig.sampling_period
t = arange(asig.t_start, asig.t_stop, dt)

# put signals in an array
signals = [asig[:,0], asig[:,1], asig[:,2], asig[:,3], asig[:,4]] 
NFFT = 512       # the length of the windowing segments
Fs = int(1.0/dt)  # the sampling frequency

fig = plt.figure()
ax1 = fig.add_subplot(2,1,1)

tick = 0

def updatefig(*args):
    global tick
    tick += 1
    print tick
    ax1.clear()
    dataset_index = tick % 5
    subplot (211)
    plot(t, signals[dataset_index])
    subplot (212)
    return specgram(signals[dataset_index], NFFT=NFFT, Fs=Fs, noverlap=500, cmap=cm.gist_heat) 

ani = animation.FuncAnimation(fig, updatefig, interval=50, blit=False)
plt.show()

