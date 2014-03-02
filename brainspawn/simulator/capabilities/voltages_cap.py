""" Voltage Capablity
Observes voltage activity within Ensembles or Neurons

*NB* - I don't actually think nengo can support these types of connections at the moment
Maybe only applies to nengo.LIF and Ensembles using those neurons?
"""

import nengo
from capability import Capability

class VoltageCap(Capability):
    """VoltageCap class
    """

    @property
    def name(self):
        return "voltages"

    def supports_obj(self, obj):
        return issubclass(obj.__class__, (nengo.Ensemble, nengo.nonlinearities.Neurons))

    def get_out_dimensions(self, obj):
        if (issubclass(obj.__class__, (nengo.Ensemble, nengo.nonlinearities.Neurons))):
            return obj.n_neurons
        else:
            raise ValueError("output_cap does not support given object")


    def connect_node(self, node, obj):
        """ Create 'simple' connection between object and neuron voltages
        Not sure if Connections will support this in current nengo impl

        See nengo.Ensemble.probe() for inspiration, also nengo.Connection

        TODO - specify filters
        """
        if (issubclass(obj.__class__, nengo.Ensemble)):
            nengo.Connection(obj.neurons.voltage, node)
        elif (issubclass(obj.__class__, nengo.nonlinearities.Neurons)):
            nengo.Connection(obj.voltage, node)
        else:
            raise ValueError("output_cap does not support given object")
