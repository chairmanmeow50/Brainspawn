""" Global constants, contains default values used throughout the application.
"""

# Size of buffer used to hold simulation data.
MAX_BUFFER_ELEMENTS = 100000

MAX_WINDOW_SIZE = 1000

# Initial size of a resize box when added to canvas
RESIZE_CONTAINER_DEFAULT_WIDTH = 300
RESIZE_CONTAINER_DEFAULT_HEIGHT = 300
# Size of the resize area in the bottom right corner of a resize box
RESIZE_BOX_WIDTH = 10
RESIZE_BOX_HEIGHT = 10
# Width of the resize area box line
RESIZE_BOX_LINE_WIDTH = 2
# Minimum size that resize boxes can be resized to
RESIZE_MIN_WIDTH = 250
RESIZE_MIN_HEIGHT = 250

# Default range of x for plots
PLOT_DEFAULT_X_WIDTH = 1

# Default step size for simulator
SIMULATOR_DEFAULT_DELTA_TIME = 0.001
# Default number of steps before redraw
SIMULATOR_DEFAULT_SIM_RATE = 6
# Default number of frames to draw per second
SIMULATOR_FRAME_RATE = 2

# File extension for layout files
LAYOUT_FILE_EXTENSION = ".bpwn"

# File extension for model files
PYTHON_FILE_EXTENSION = "py"
# Name of model files in save/open dialogs
PYTHON_FILE_EXTENSION_NAME = "Python files"

# Size of controller panel in main frame
CONTROLLER_PANEL_WIDTH = 300
CONTROLLER_PANEL_HEIGHT = 50

# Border padding of the customize window
CUSTOMIZE_WINDOW_BORDER_WIDTH = 10
# Customize window button size
CUSTOMIZE_WINDOW_BUTTON_WIDTH = 80
CUSTOMIZE_WINDOW_BUTTON_HEIGHT = 20
# Title for customize window
CUSTOMIZE_WINDOW_TITLE = "Customize"

# Maximum unsigned float value, used in converting colour values
MAX_UNSIGNED_SHORT_FLOAT = 65535.0

# GTK enum for right click
EVENT_BUTTON_RIGHT_CLICK = 3

# Default size of visualizer
VISUALIZER_WIDTH = 800
VISUALIZER_HEIGHT = 600
# Default timer interval for GUI timer, drives simulator
VISUALIZER_TIMER_INTERVAL = 1

# Default title of visualizer
MAIN_FRAME_TITLE = "Nengo Visualizer"
