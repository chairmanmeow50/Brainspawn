import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np

dt = 0.0005
t = np.arange(0.0, 20.0, dt)
s1 = np.sin(2 * np.pi * 100 * t)
s2 = 2 * np.sin(2 * np.pi * 400 * t)

# create a transient "chirp"
mask = np.where(np.logical_and(t > 10, t < 12), 1.0, 0.0)
s2 = s2 * mask

# add some noise into the mix
noise = 0.01 * np.random.randn(len(t))

x = s1 + s2 + noise  # the signal
ax1 = plt.subplot(211)
plt.plot(t, x)

# Pxx is the segments x freqs array of instantaneous power
# freqs is the frequency vector
# bins are the centers of the time bins in which the power is computed
# im is the matplotlib.image.AxesImage instance
plt.subplot(212, sharex=ax1)
NFFT = 1024         # the length of the windowing segments
Fs = int(1.0 / dt)  # the sampling frequency
Pxx, freqs, bins, im = plt.specgram(x, NFFT=NFFT, Fs=Fs, noverlap=900, cmap=cm.gist_heat)

plt.show()
