import spa
import nengo.nef_theano as nef
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Rules:
    def A(state='A'):
        effect(state='B')
    def B(state='B'):
        effect(state='C')
    def C(state='C'):
        effect(state='D')
    def D(state='D'):
        effect(state='E')
    def E(state='E'):
        effect(state='A')

class Sequence(spa.SPA):
    dimensions = 8
    verbose = True

    state = spa.Buffer()
    BG = spa.BasalGanglia(Rules)
    thal = spa.Thalamus(BG)

    input = spa.Input(0.1,state='D')

net = nef.Network('Sequence', seed=1)
seq = Sequence(net)

pThal = net.make_probe('thal.rule', dt_sample=0.001)
pGPi = net.make_probe('BG.GPi', dt_sample=0.001, data_type='spikes')
pState = net.make_probe('state.buffer', dt_sample=0.001, data_type='spikes')

net.run(1)

dt = 0.001
t = np.arange(0.0, net.run_time, dt)
x = pThal.get_data()[:,0]  # the signal

fig = plt.figure()

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

def animate(i):
	net.run(.01)

	x = pThal.get_data()[:,0]  # the signal
	t = np.linspace(0.0, net.run_time, x.size)
	plt.subplot(211)
	plt.plot(t, x)
	plt.subplot(212, sharex=ax1)
	NFFT = 1024         # the length of the windowing segments
	Fs = int(1.0 / dt)  # the sampling frequency
	return plt.specgram(x, NFFT=NFFT, Fs=Fs, noverlap=900, cmap=cm.gist_heat)

ani = animation.FuncAnimation(fig, animate, interval=10)

plt.show()
