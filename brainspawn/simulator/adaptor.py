""" Adaptor module.

Responsible for creating custom nodes for storing viewable data,
and connecting them to the observed object.

The nodes are added to the model, and this step should be done
prior to passing the model to the simulator.

Views can then subscribe to be updated with the given data,
according to the given type of data ("capabilities").

Observed data is stored in circular buffers of configurable size,

NOTE - As implemented, we don't support watching objects with an
output signal of zero dimensions.

"""

import collections
import nengo
import numpy as np
from capabilities.cap_factory import CapFactory
import settings


class OutputFn(collections.Callable):
    """ Callable which is passed to a given node.

    TODO: could this be rewritten clearer?
    The callable is called by the Node during simulation with inputs
    of given dimension, writes the data to the buffer, if the cap is
    connected, and publishes the updated buffer.
    """

    def __init__(self, sim_manager, dimensions):
        """ Sets up simulator manager.
        Creates buffers for data.
        """
        self.sim_manager = sim_manager
        self.dimensions = dimensions
        self.buffer = None
        self.buffer_start_step = None
        self.subscribed_fns = []

    def __call__(self, time, input_signal):
        """ Called by Node with data of interest.
        If we have subscriptions, store data and publish.

        Params as passed by the simulator.
        :param time: The simulated time of the step.
        :param input_signal: The numpy ndarray representing the input signal.

        Sets buffer_start_step if necessary.
        """
        if (self.subscribed_fns):
            self.buffer.append_data(input_signal)
            if (self.buffer_start_step is None):
                self.buffer_start_step = self.sim_manager.current_step
            self.update_all()

    def update_all(self):
        """ Calls the update function for all
        subscribed functions in self.subscribed_fns.
        """
        for fn in self.subscribed_fns:
            self.update(fn)

    def update(self, fn):
        """ Updates with data in a specific range,
        starting at the beginning of the buffer to the current simulation
        step.
        """
        if (self.buffer and self.buffer_start_step is not None):
            start_step = max(self.buffer_start_step,
                             self.sim_manager.current_step -
                             settings.MAX_WINDOW_SIZE)
            start_idx = start_step - self.buffer_start_step
            end_idx = max(self.sim_manager.current_step -
                          self.buffer_start_step, 0)
            data = self.buffer.get_data()[start_idx:end_idx]
            fn(start_step, self.sim_manager.dt, data)

    def reset(self):
        """ Resets data buffers, and calls update once
        with empty data buffers.
        """
        if self.buffer:
            self.buffer.reset()
            self.buffer_start_step = None
            for fn in self.subscribed_fns:
                    fn(0, self.sim_manager.dt, self.buffer.get_data())

    def subscribe(self, fn):
        """ Subscribes fn.
        Creates data buffer if necessary.
        Updates with current data.
        """
        if (not self.buffer):
            self.buffer = Buffer(self.dimensions)
        self.subscribed_fns.append(fn)
        self.update(fn)

    def unsubscribe(self, fn):
        """ Unsubscribes fn.
        Removes data buffer, and resets start time if necessary.
        """
        self.subscribed_fns.remove(fn)
        if (not self.subscribed_fns):
            self.buffer = None
            self.buffer_start_step = None


class Buffer(object):
    """ Circular Buffer for storing data.

    Buffer takes up max_size*2*dimensions*sizeof(data.dtype) space in memory.
    """

    def __init__(self, dimensions):
        """ Initializes buffer.
        """
        self.max_size = settings.MAX_BUFFER_ELEMENTS
        self.data = np.empty([self.max_size*2, dimensions])
        self.window_start = 0
        self.size = 0

    def append_data(self, in_data):
        """Appends data to end of buffer.
        numpy raises ValueError if dimensions of data are incorrect.
        """
        i = (self.window_start + self.size) % self.max_size
        self.data[i] = in_data
        self.data[i+self.max_size] = in_data
        if (self.size < self.max_size):
            self.size += 1
        else:
            self.window_start = (self.window_start + 1) % self.max_size

    def get_data(self):
        """ Returns a view of the contents of the buffer.
        """
        return self.data[self.window_start:self.size]

    def reset(self):
        """ Resets window start and size.
        """
        self.window_start = 0
        self.size = 0


class Adaptor(object):
    """ Class for observing an object in a network.

    For a given object, creates a node to observe each capability we have for
    the object.
    Views can then subscribe to data from that node.
    Data is buffered only if we have at least one subscription to data.
    """

    def __init__(self, sim_manager, obj):
        """ Initializes adapter, adds all supported capabilities and
        connects to simulator manager.
        """
        self.caps = []
        self.out_fns = {}
        self.obj = obj
        capabilites = self._load_caps()
        for cap in capabilites:
            if (cap.supports_obj(obj)):
                self.caps.append(cap)
        self._connect_obj(sim_manager)

    def _load_caps(self):
        """ Load capabilities.
        """
        return CapFactory.get_caps()

    def _connect_obj(self, sim_manager):
        """ Create Nodes to observe data, and connect them to observed object.

        NOTE:
        When the model is given to the simulator, the simulator
        creates a deep copy of the given model in order to perform simulations
        on.
        If we just pass our OutputFn callable, it gets deep copied, and we are
        unable to subscribe to the new copied OutputFn.

        Our sort of hacky way of getting around this is to wrap the callable
        in a lambda (which is atomic, so gets around the deep copy), and pass
        the desired callable as a default kwarg to the lambda.

        TODO: OutputFn probably no longer needs to be a callable, we should
        change this and rename it.
        """
        for cap in self.caps:
            dimensions = cap.get_out_dimensions(self.obj)
            self.out_fns[cap] = OutputFn(sim_manager, dimensions)
            obj_name = self.obj.name if hasattr(self.obj, 'name') else \
                self.obj.__class__.__name__
            label = cap.name + '(' + obj_name + ')'
            # see the documentation of this function for an explanation
            node = nengo.Node(output=lambda time, data, fn=self.out_fns[cap]:
                              fn(time, data), size_in=dimensions, label=label)
            cap.connect_node(node, self.obj)

    def subscribe(self, cap, fn):
        """ Subscribe to given cap.
        fn will be called at each step with updated numpy array
        containing data from the node.
        """
        self.out_fns[cap].subscribe(fn)

    def unsubscribe(self, cap, fn):
        """ Unsubscribe function from cap.
        Removes subscription to function,
        or does nothing if fn was not subscribed.
        """
        self.out_fns[cap].unsubscribe(fn)

    def update_all(self):
        """ Calls update_all on all OutputFn objects.
        """
        for cap, out_fn in self.out_fns.items():
            out_fn.update_all()

    def reset(self):
        """ Calls reset on all OutputFn objects.
        """
        for cap, out_fn in self.out_fns.items():
            out_fn.reset()
