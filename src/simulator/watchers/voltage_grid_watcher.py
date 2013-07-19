from nengo_theano import probe
from watcher import Watcher
from old_plots import Voltage_Grid_Plot
import numpy

class Voltage_Grid_Watcher(Watcher):
    """
    """

    def check(self, obj):
        return isinstance(obj, probe.Probe)

    def views(self, obj):
        assert isinstance(obj, probe.Probe)
        r = [('Voltage Grid', Voltage_Grid_Plot,
            dict(func=self.value, label="Voltage Grid",
                Fs=1.0 / obj.dt_sample))]
        return r

    def value(self, obj):
        data = obj.get_data()
        print(data[len(data)-1, 0])
        return data[len(data)-1] # Can probably do this differently with proper slicing
