""" Spikes Capablity
Observes spiking activity in Ensembles and Neurons

Not sure if nengo supports Neurons yet though
"""

import nengo
import numpy as np
from capability import Capability

class SpikesCap(Capability):
    """Spikes Capability
    """

    @property
    def name(self):
        return "spikes"

    def supports_obj(self, obj):
        return issubclass(obj.__class__, (nengo.Ensemble, nengo.nonlinearities.Neurons))

    def get_out_dimensions(self, obj):
        if (issubclass(obj.__class__, (nengo.Ensemble, nengo.nonlinearities.Neurons))):
            return obj.n_neurons
        else:
            raise ValueError("output_cap does not support given object")


    def connect_node(self, node, obj):
        """ Create connection between object and neurons, with identity transform

        See nengo.Ensemble.probe() for inspiration, also nengo.Connection

        TODO - specify filters
        """
        #probe = nengo.Probe(obj, "spikes")
        if (issubclass(obj.__class__, nengo.Ensemble)):
            nengo.Connection(obj.neurons, node, filter=None, transform=np.eye(obj.n_neurons))
        elif (issubclass(obj.__class__, nengo.nonlinearities.Neurons)):
            nengo.Connection(obj, node, filter=None, transform=np.eye(obj.n_neurons))
        else:
            raise ValueError("output_cap does not support given object")

