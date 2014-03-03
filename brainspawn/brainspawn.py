#!/usr/bin/env python
"""Main app
"""

from gi import pygtkcompat
pygtkcompat.enable()
pygtkcompat.enable_gtk(version="3.0")
import gtk

from controller.visualizer_controller import VisualizerController

def main():
    app = VisualizerController()
    gtk.main()

if __name__ == '__main__':
    main()
