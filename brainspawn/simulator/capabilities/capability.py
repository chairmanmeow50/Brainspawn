""" Abstract base class for Capabilites
Essentially a 'data type'
Capability represents observable data that a given object
in a nengo model has to offer.  The capablity defines how
to connect an observer node to the object to be observed
in order to collect the data. It also maintains some
metadata regarding the type of data offered, including
determining the dimensions of the given data from the given
object.
"""

from abc import ABCMeta, abstractmethod

class Capability(object):
    """Capability class
    """

    @property
    def name(self):
        """
        Name of the cap.  Should be unique, like an id,
        but we don't enforce this at the moment
        """
        return "Capability"

    def supports_obj(self, obj):
        """ Determines if the given object offers this cap

        Args:
            obj (object): The object to check

        Returns:
            bool.  True if given object offers this capability
        """
        return False

    @abstractmethod
    def get_out_dimensions(self, obj):
        """ Get the output dimensions of this cap for the given object

        Args:
            obj (object): The object offering the cap

        Returns:
            int.  The number of dimensions of the data offered by
            this cap for this obj

        Raises:
            ValueError - This is not a cap for the given object

        The output dimensions depend on the object and the capability.
        Also note here that dimensions are *not* like numpy ndarray dimensions,
        they are simply the length of the vector that the signal will be.
        I know.  Threw me for a bit of a loop as well.
        """
        pass

    @abstractmethod
    def connect_node(self, node, obj):
        """ Connects an observer node to the given object

        Args:
            node (nengo.Node): The observer node to connect to the object
            obj (object): The object to observe

        Raises:
            ValueError - This is not a cap for the given object

        """
        pass

