#!/usr/bin/env python

import gtk
from gi.repository import Gtk
from gi.repository import GObject
import math
import glob
import imp
import traceback

from view.components.input_panel import Input_Panel
from view.components.controller_panel import Controller_Panel
from view.components.menu_bar import Menu_Bar
from view.components.resize_box import ResizeBox
import simulator.sim_manager

from matplotlib.backends.backend_gtk3 import TimerGTK3


# Fix for a method that is not properly introspected
_child_get_property = Gtk.Container.child_get_property
def child_get_property(self, child, name):
    v = GObject.Value()
    v.init(int)
    _child_get_property(self, child, name, v)
    return v.get_int()
Gtk.Container.child_get_property = child_get_property


class MainFrame:
    def __init__(self, sim_manager, controller):
        self.sim_manager = sim_manager
        self.controller = controller

        self.vbox = gtk.VBox(False, 0)
        self.playing = False
        self.press = None
        self.resize = False
        self.resize_info = None

        self.all_canvas = []

        # create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_default_size(800, 600)
        self.window.set_title("Nengo Visualizer")
        self.window.connect("delete_event", lambda w,e: gtk.main_quit())

        self.input_panel = Input_Panel(self)
        self.controller_panel = Controller_Panel(self)
        self.menu_bar = Menu_Bar(self, controller)

        self.layout_event_box = gtk.EventBox()
        self.canvas_layout = gtk.Layout()
        self.layout_event_box.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#ffffff"))
        self.layout_event_box.connect("button_release_event", controller.on_layout_button_release)

        # Used to control framerate for redrawing graph components
        self.sim_rate = 6 # rate at which we call sim.step()
        self.framerate = 2
        self.next_gcomponent_redraw = 0

        # pretend new_timer is a static method
        self.timer = TimerGTK3(interval=1)
        self.timer.add_callback(self.step)
        self.timer.single_shot = True

        self.vbox.pack_start(self.menu_bar, False, False, 0)
        self.vbox.pack_start(self.controller_panel, False, False, 0)

        self.layout_event_box.add(self.canvas_layout)

        self.vbox.pack_start(self.layout_event_box, True, True, 0)

        self.window.add(self.vbox)

        self.window.show_all()
        
        self.controller_panel.toggle_play(False)

    def hscale_change(self, range, scroll, value):
        self.sim_manager.current_step = value
        self.update_canvas()

    # Move some of this functionality to the controller
    def step(self):
        if (self.playing == True):
            self.sim_manager.step()

            self.controller_panel.update_slider(self.sim_manager.min_step, self.sim_manager.last_sim_step,
                                                self.sim_manager.current_step, self.sim_manager.dt)

            if (self.next_gcomponent_redraw == 0):
                self.update_canvas()
                self.next_gcomponent_redraw = self.sim_rate/self.framerate
            else:
                self.next_gcomponent_redraw -= 1

            self.timer.start(1)

    def update_canvas(self):
        map(lambda canvas:canvas.queue_draw(), self.all_canvas)

    #Controller code for controller_panel
    def format_slider_value(self, scale, value):
        return '%.3f' % (value * self.sim_manager.dt)

    def play_pause_button(self, widget):
        if (self.playing == True):
            self.timer.stop()
            self.playing = False
            self.controller_panel.toggle_play(self.playing)
        else:
            self.timer.start(1)
            self.playing = True
            self.controller_panel.toggle_play(self.playing)

    def reset_button(self, widget):
        self.timer.stop()
        self.playing = False
        self.controller_panel.toggle_play(False)
        
        self.controller_panel.hscale_adjustment.set_lower(0)
        self.controller_panel.hscale_adjustment.set_upper(0)
        self.controller_panel.update_slider(0, 0, 0, self.sim_manager.dt)
        self.sim_manager.reset()
        self.jump_to(widget, self.sim_manager.min_step)

    def jump_to_front(self, widget):
        self.jump_to(widget, self.sim_manager.min_step)

    def jump_to(self, widget, value):
        self.playing = True
        self.play_pause_button(widget)
        self.sim_manager.current_step = value
        self.controller_panel.set_slider(self.sim_manager.current_step)
        self.update_canvas()

    def jump_to_end(self, widget):
        self.jump_to(widget, self.sim_manager.last_sim_step)

    def button_press(self, widget, event):
        if event.type == gtk.gdk.BUTTON_PRESS:
            widget.popup(None, None, None, event.button, event.time)
            # Tell calling code that we have handled this event the buck
            # stops here.
            return True
        # Tell calling code that we have not handled this event pass it on.
        return False

    # Print a string when a menu item is selected
    def menuitem_response(self, widget, string):
        print "%s" % string

    def show_plot(self, canvas, center=False):
        resize_box = ResizeBox(canvas, self.canvas_layout)
        self.all_canvas.append(resize_box.get_canvas())
        if (center):
            x = (self.window.get_allocated_width() - resize_box.get_width()) / 2
            y = (self.canvas_layout.get_allocated_height() - resize_box.get_height()) / 2
            self.canvas_layout.put(resize_box, x, y)
            resize_box._pos_x = x
            resize_box._pos_y = y
        else:
            self.canvas_layout.put(resize_box, 0, 0)

    def remove_plot(self, canvas):
        self.all_canvas.remove(canvas)
        self.canvas_layout.remove(canvas.get_parent())

    def toggle_panel(self, widget, panel):
        if (widget.get_active()):
            panel.set_visible(True)
            self.control_panel.add(panel)
        else:
            panel.set_visible(False)
            self.control_panel.remove(panel)

