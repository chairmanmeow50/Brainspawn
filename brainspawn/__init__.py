#

NAME = 'brainspawn'
__version__ = '0.1'

import gtk
from brainspawn.controller.visualizer_controller import VisualizerController

def main():
    app = VisualizerController()
    gtk.main()
