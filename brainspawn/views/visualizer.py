#!/usr/bin/env python
"""Visualizer class. Contains GUI control methods as well 
constructor for main frame.
"""
import gtk
from gi.repository import Gtk
from gi.repository import GObject
import math
import glob
import imp
import traceback

from views.components.input_panel import Input_Panel
from views.components.controller_panel import Controller_Panel
from views.components.menu_bar import Menu_Bar
from views.components.resize_box import ResizeBox
import simulator.sim_manager

from matplotlib.backends.backend_gtk3 import TimerGTK3
import settings

# Fix for a method that is not properly introspected
_child_get_property = Gtk.Container.child_get_property
def child_get_property(self, child, name):
    v = GObject.Value()
    v.init(int)
    _child_get_property(self, child, name, v)
    return v.get_int()
Gtk.Container.child_get_property = child_get_property

class MainFrame:
    """ Main frame for visualizer
    """
    def __init__(self, sim_manager, controller):
        """ Sets up frame. Creates controller panel, GTK window,
        layout canvas, GTK timer and event boxes.
        """
        self.sim_manager = sim_manager
        self.controller = controller

        self.vbox = gtk.VBox(False, 0)
        self.playing = False
        self.press = None
        self.resize = False
        self.resize_info = None

        self.resize_boxes = {}

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_default_size(settings.VISUALIZER_WIDTH, 
                                     settings.VISUALIZER_HEIGHT)
        self.window.set_title(settings.MAIN_FRAME_TITLE)
        self.window.connect("delete_event", self.on_quit)

        self.input_panel = Input_Panel(self)
        self.controller_panel = Controller_Panel(self)
        self.menu_bar = Menu_Bar(self, controller)

        self.layout_event_box = gtk.EventBox()
        self.canvas_layout = gtk.Layout()
        self.layout_event_box.modify_bg(gtk.STATE_NORMAL, 
                                        gtk.gdk.color_parse("#ffffff"))
        self.layout_event_box.connect("button_release_event", 
                                      controller.on_layout_button_release)

        # Used to control frame rate for redrawing graph components
        # rate at which we call sim.step()
        self.sim_rate = settings.SIMULATOR_DEFAULT_SIM_RATE 
        self.framerate = settings.SIMULATOR_FRAME_RATE
        self.next_gcomponent_redraw = 0

        # set up timer
        self.timer = TimerGTK3(interval=settings.VISUALIZER_TIMER_INTERVAL)
        self.timer.add_callback(self.step)
        self.timer.single_shot = True

        self.vbox.pack_start(self.menu_bar, False, False, 0)
        self.vbox.pack_start(self.controller_panel, False, False, 0)

        self.layout_event_box.add(self.canvas_layout)

        self.vbox.pack_start(self.layout_event_box, True, True, 0)

        self.window.add(self.vbox)

        self.window.show_all()

        self.controller_panel.toggle_play(False)

    def on_quit(self, widget, event):
        """ Event handler for quit event
        """
        self.controller.on_quit()
        gtk.main_quit()

    def hscale_change(self, range, scroll, value):
        """ Event handler for seek bar value change events
        """
        if value < self.sim_manager.min_step or \
           value > self.sim_manager.last_sim_step:
            return
        self.sim_manager.current_step = value
        self.update_canvas()

    def step(self):
        """ Step function which sets up a timer that triggers more tick events.
        Updates canvas if redraw is needed.
        """
        if (self.playing == True):
            self.sim_manager.step()

            self.controller_panel.update_slider(self.sim_manager.min_step, 
                                                self.sim_manager.last_sim_step,
                                                self.sim_manager.current_step, 
                                                self.sim_manager.dt)

            if (self.next_gcomponent_redraw == 0):
                self.update_canvas()
                self.next_gcomponent_redraw = self.sim_rate/self.framerate
            else:
                self.next_gcomponent_redraw -= 1

            self.timer.start(settings.VISUALIZER_TIMER_INTERVAL)

    def update_canvas(self):
        """ Calls queue_draw on canvas layout.
        """
        self.canvas_layout.queue_draw()

    def format_slider_value(self, scale, value):
        """ Formatting slider text value.
        Returns a 3 digit float string.
        """
        return '%.3f' % (value * self.sim_manager.dt)

    def play_pause_button(self, widget):
        """ Toggles play or pause for simulation.
        """
        if (self.playing == True):
            self.timer.stop()
            self.playing = False
            self.controller_panel.toggle_play(self.playing)
            self.update_canvas()
        else:
            self.timer.start(settings.VISUALIZER_TIMER_INTERVAL)
            self.playing = True
            self.controller_panel.toggle_play(self.playing)

    def reset_button(self, widget):
        """ Resets controller panel state, pauses simulation, 
        sets time step to beginning.
        """
        self.timer.stop()
        self.playing = False
        self.controller_panel.toggle_play(False)

        self.controller_panel.hscale_adjustment.set_lower(0)
        self.controller_panel.hscale_adjustment.set_upper(0)
        self.controller_panel.update_slider(0, 0, 0, self.sim_manager.dt)
        self.sim_manager.reset()
        self.jump_to(widget, self.sim_manager.min_step)

    def jump_to_front(self, widget):
        """ Jumps to beginning of simulation.
        """
        self.jump_to(widget, self.sim_manager.min_step)

    def jump_to(self, widget, value):
        """ Jumps to given time step of simulation.
        """
        self.playing = True
        self.play_pause_button(widget)
        self.sim_manager.current_step = value
        self.controller_panel.set_slider(self.sim_manager.current_step)
        self.update_canvas()

    def jump_to_end(self, widget):
        """ Jumpts to last time step of simulation.
        """
        self.jump_to(widget, self.sim_manager.last_sim_step)

    def on_button_release(self, widget, event):
        """ TODO: is this needed to fix a behaviour?
        ie. the problem with context menus disappearing
        """
        if event.type == gtk.gdk.BUTTON_PRESS:
            widget.popup(None, None, None, event.button, event.time)
            # Return true to stop event propagation
            return True
        return False

    def show_plot(self, plot, center=False, position=None, size=None):
        """ Creates ResizeBox from plot, centers plot if center boolean 
        is set. Otherwise, move to position specified. If no position 
        is specified, set position to 0,0 (top left). 
        
        Set size if specified.
        """
        resize_box = ResizeBox(plot, self.canvas_layout)
        self.canvas_layout.put(resize_box, 0, 0)
        self.resize_boxes[plot] = resize_box

        if (center):
            x = (self.window.get_allocated_width() - 
                 resize_box.get_width()) / 2
            y = (self.canvas_layout.get_allocated_height() - 
                 resize_box.get_height()) / 2
        elif position:
            x, y = position
        else:
            x = 0
            y = 0
        resize_box.set_position(x, y)

        if size:
            resize_box.set_size(*size)

        plot.apply_config()

    def remove_plot(self, plot):
        """ Remove plot from list of plots.
        """
        self.canvas_layout.remove(self.resize_boxes[plot])
        # TODO: is this needed?
        del self.resize_boxes[plot]

    def get_item_position(self, item):
        """ Return position of item in list of resize_boxes.
        """
        return (self.resize_boxes[item].pos_x, self.resize_boxes[item].pos_y)

    def get_item_size(self, item):
        """ Return size of element item in resize_boxes.
        """
        return (self.resize_boxes[item].get_width(), 
                self.resize_boxes[item].get_height())

    def set_item_position(self, item, position):
        """ Sets position for element item in resize_boxes.
        """
        x, y = position
        self.resize_boxes[item].set_position(x, y)

    def set_item_size(self, item, size):
        """ Sets size for element item in resize_boxes.
        """
        w, h = size
        self.resize_boxes[item].set_size(w, h)

