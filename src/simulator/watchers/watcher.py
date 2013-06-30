class Watcher:

    def check(self, obj):
        """
        Should return True if the given object is an instance
        of the class associated with this watch.
        """
        return False

    def views(self, obj):
        """
        Should return a list of 3-tuples, where each tuple
        consists of a string label, a display component (from timeview.components)
        and a dict giving a list of arguments for that component.
        """
        return [(None, None, None)]

    def priority(self):
        """
        Return a number indicating the priority level of this watcher (this only affects the
        display, where it is used to sort the views of the watcher).  0 is the highest priority,
        then 1, 2, etc.
        """
        return 100
