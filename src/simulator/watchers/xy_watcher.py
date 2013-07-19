from nengo_theano import probe
from watcher import Watcher
from old_plots import XY_Plot
import numpy

class XYWatcher(Watcher):
    """
    """

    def check(self, obj):
        return isinstance(obj, probe.Probe)

    def views(self, obj):
        assert isinstance(obj, probe.Probe)
        r = [('XY', XY_Plot,
            dict(func=self.value, label="XY",
                Fs=1.0 / obj.dt_sample))]
        return r

    def value(self, obj):
        data = obj.get_data()
        print(data[len(data)-1, 0])
        return numpy.array([data[len(data) - 1, 0]]) # Can probably do this differently with proper slicing
