#!/usr/bin/env python
"""Main app
"""

import gtk

from controller.visualizer_controller import VisualizerController

def main():
    app = VisualizerController()
    gtk.main()

if __name__ == '__main__':
    main()
