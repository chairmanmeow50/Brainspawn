#!/usr/bin/env python
"""Main app
"""

from gi import pygtkcompat
pygtkcompat.enable()
pygtkcompat.enable_gtk(version="3.0")
import gtk
import sys

import warnings
warnings.filterwarnings("ignore", "tight_layout : falling back to Agg renderer")

from simulator.sim_manager import SimManager
from controllers.visualizer_controller import VisualizerController

def main():
    sim_manager = SimManager()
    if len(sys.argv) > 1:
        model_file = sys.argv[1]
        if model_file.endswith(".py"):
            controller = VisualizerController(sim_manager, model_file)
    else:
        controller = VisualizerController(sim_manager)

    gtk.main()

if __name__ == '__main__':
    main()
