#!/usr/bin/env python
"""Main app
"""

from gi import pygtkcompat
pygtkcompat.enable()
pygtkcompat.enable_gtk(version="3.0")
import gtk
import sys

from simulator.sim_manager import SimManager
from controllers.visualizer_controller import VisualizerController

def main():
    sim_manager = SimManager()
    if (len(sys.argv) > 0):
        arg1 = sys.argv[1]
        if (arg1.endswith(".py")):
            controller = VisualizerController(sim_manager, arg1)
    else:
        controller = VisualizerController(sim_manager)

    gtk.main()

if __name__ == '__main__':
    main()
