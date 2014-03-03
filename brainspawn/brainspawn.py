#!/usr/bin/env python
"""Main app
"""

from gi import pygtkcompat
pygtkcompat.enable()
pygtkcompat.enable_gtk(version="3.0")
import gtk

from simulator.sim_manager import SimManager
from controller.visualizer_controller import VisualizerController

def main():
    sim_manager = SimManager()
    controller = VisualizerController(sim_manager)

    gtk.main()

if __name__ == '__main__':
    main()
