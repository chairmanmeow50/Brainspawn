import nengo
import copy
from adaptor import Adaptor, max_buffer_elements
from capabilities.cap_factory import CapFactory

class SimManager(object):
    """
    Class for managing interaction with the simulator
    """

    def __init__(self):
        self.min_step = 0
        self.last_sim_step = 0
        self._current_step = 0
        self.adaptors = {}
        self.max_buffer_elements = max_buffer_elements

    @property
    def current_step(self):
        return self._current_step

    @current_step.setter
    def current_step(self, value):
        self._current_step = value
        self.update_all()

    def _has_caps(self, obj):
        """ Returns true if we have caps that support the given obj
        """
        supported_caps = [cap for cap in CapFactory.get_caps() if cap.supports_obj(obj)]
        if supported_caps:
            return True
        else:
            return False

    def load_new_model(self, model, dt):
        """ Processes a model for visualization and simulation
        Adds adaptor to each object in the model,
        initializes simulator with model

        Note: We modify the model, so you probably want to make
        a copy of it first.
        """
        self.model = model
        self.dt = dt
        self.adaptors = {}
        for obj in list(self.model.objs): # copy list! connect() adds objs to model
            if (self._has_caps(obj)):
                self.adaptors[obj] = Adaptor(self, obj)
        self.sim = nengo.Simulator(self.model, self.dt)

    def get_caps_for_obj(self, obj):
        """
        Returns capabilites of adaptor for given object,
        or an empty list if object is not an object in our
        currrently loaded model for which we have an adaptor
        """
        if (obj not in self.adaptors):
            return []
        else:
            return self.adaptors[obj].caps

    def connect_to_obj(self, obj, cap, fn):
        """
        Connects a view to an object for a given cap,
        throws ValueError if this is not possible.
        Creates a buffer for the object, cap if necessary,
        and connects the view to the given buffer
        """
        if (obj not in self.adaptors or cap not in self.adaptors[obj].caps):
            raise ValueError('Cannot connect view to object')
        self.adaptors[obj].subscribe(cap, fn)

    def disconnect_from_obj(self, obj, cap, fn):
        """
        Disconnects a function from an object
        """
        self.adaptors[obj].unsubscribe(cap, fn)

    def step(self):
        """
        Advances SimManager by 1 step,
        runs simulator if necessary
        """
        if (self._current_step > self.last_sim_step):
            self.sim.step()
            self.min_step = max(0, self.last_sim_step -
                    self.max_buffer_elements + 1)
            self.last_sim_step += 1
        else:
            self.update_all()
        self._current_step += 1

    def update_all(self):
        for obj, adaptor in self.adaptors.items():
            adaptor.update_all()

    def reset(self):
        """
        Resets Simulator
        """
        self.min_step = 0
        self.last_sim_step = 0
        self._current_step = 0
        self.sim = nengo.Simulator(self.model, self.dt)
        for obj, adaptor in self.adaptors.items():
            adaptor.reset()

