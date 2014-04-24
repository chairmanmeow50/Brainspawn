#!/usr/bin/env python
"""Launcher for Brainspawn visualization application.
"""

from gi import pygtkcompat
pygtkcompat.enable()
pygtkcompat.enable_gtk(version="3.0")
import gtk
import sys

import warnings
# Suppress some expected warnings
warnings.filterwarnings("ignore",
                        "tight_layout : falling back to Agg renderer")

from simulator.sim_manager import SimManager
from controllers.visualizer_controller import VisualizerController
import settings


def main():
    """ Instantiates simulation manager. Checks for a model file in arguments,
    if command line argument exists, attempt to load that model file directly.
    Then instantiate visualizer controller.
    """
    sim_manager = SimManager()
    if len(sys.argv) > 1:
        model_file = sys.argv[1]
        if model_file.endswith(settings.PYTHON_FILE_EXTENSION):
            controller = VisualizerController(sim_manager, model_file)
    else:
        controller = VisualizerController(sim_manager)

    gtk.main()

if __name__ == '__main__':
    main()
