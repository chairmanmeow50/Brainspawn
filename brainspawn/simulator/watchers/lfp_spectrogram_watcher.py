from nengo_theano import probe
from watcher import Watcher
from view.components import spectrogram
import numpy

class LFPSpectrogramWatcher(Watcher):
    """
    This will need to be changed once we discover what the
    LFP Spectrogram should actually show
    """

    def check(self, obj):
        return isinstance(obj, probe.Probe)

    def views(self, obj):
        assert isinstance(obj, probe.Probe)
        r = [('LFP Spectrogram', spectrogram.Spectrogram,
            dict(func=self.value, label="LFP Spectrogram",
                Fs=1.0 / obj.dt_sample))]
        return r

    def value(self, obj):
        data = obj.get_data()
        print(data[len(data)-1, 0])
        return numpy.array([data[len(data) - 1, 0]]) # Can probably do this differently with proper slicing
