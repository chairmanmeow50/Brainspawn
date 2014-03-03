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
import simulator.sim_manager

# FIXME For now
from view.visualizations.dogeplot import DogePlot
from view.visualizations.xy_plot import XYPlot
from view.visualizations.firing_rate import Firing_Rate_Plot
from view.visualizations.voltage_grid import Voltage_Grid_Plot
import sample_networks.two_dimensional_rep as example

from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas


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

        self.all_plots = [] # TODO - Move plots to controller
        self.all_canvas = []

        # TODO - Replace with "add_plot functionality in controller"
        plot_obj = XYPlot(self.sim_manager, self.controller, rows=10, columns=10)
        self.add_plot(plot_obj)
        self.all_plots.append(plot_obj)
        self.all_canvas.append(plot_obj.canvas)
        self.xy_plot = plot_obj

        # Also add to add_plot in controller
        map(lambda x:x.mpl_connect('figure_enter_event', self.enter_figure), self.all_canvas)
        map(lambda x:x.mpl_connect('figure_leave_event', self.leave_figure), self.all_canvas)
        map(lambda x:x.mpl_connect('button_press_event', self.mouse_on_press), self.all_canvas)
        map(lambda x:x.mpl_connect('button_release_event', self.mouse_on_release), self.all_canvas)
        map(lambda x:x.mpl_connect('motion_notify_event', self.mouse_on_motion), self.all_canvas)

        # create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_default_size(800, 600)
        self.window.set_title("Nengo Python Visualizer")
        self.window.connect("delete_event", lambda w,e: gtk.main_quit())

        self.input_panel = Input_Panel(self)
        self.controller_panel = Controller_Panel(self)
        self.menu_bar = Menu_Bar(self, controller)

        self.canvas_layout = gtk.Layout()
        self.canvas_layout.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#ffffff"))

        # hmm...
        figure = self.all_plots[0].figure

        # Used to control framerate for redrawing graph components
        self.sim_rate = 6 # rate at which we call sim.step()
        self.framerate = 2
        self.next_gcomponent_redraw = 0

        self.canvas = FigureCanvas(figure)  # a gtk.DrawingArea
        self.timer = self.canvas.new_timer(interval=1000/self.sim_rate)
        self.timer.add_callback(self.step)

        self.vbox.pack_start(self.menu_bar, False, False, 0)
        self.vbox.pack_start(self.controller_panel, False, False, 0)

        self.vbox.pack_start(self.canvas_layout, True, True, 0)

        self.window.add(self.vbox)

        self.window.show_all()

        self.show_plot(self.all_plots[0])

    def add_plot(self, plot):
        """ COMPLETELY PLACEHOLDER AT THE MOMENT
        Will move func to controller
        """
        node_caps = self.sim_manager.get_caps_for_obj(example.neurons)
        for cap in node_caps:
            #print (cap.name, cap.get_out_dimensions(example.neurons))
            if (cap.name is plot.out_cap()):
                out_cap = cap
        #print "connected " + plot.name() + " with cap " + plot.out_cap()
        self.sim_manager.connect_to_obj(example.neurons, out_cap, plot.update)

    def toggle_resize(self, widget):
        if (widget.get_active()):
            self.resize = True
        else:
            self.resize = False

    def mouse_on_press(self, event):
        canvas = event.canvas
        x0 = self.canvas_layout.child_get_property(canvas, "x")
        y0 = self.canvas_layout.child_get_property(canvas, "y")
        widget_x, widget_y = self.canvas_layout.get_pointer()
        self.press = x0, y0, widget_x, widget_y

    def mouse_on_motion(self, event):
        if self.press is None: return

        x0, y0, xpress, ypress = self.press
        owidth, oheight = event.canvas.get_width_height()

        canvas_layout_x, canvas_layout_y = self.canvas_layout.get_pointer()

        if (self.resize):
            if (self.resize_info == None):
                self.resize_info = xpress, ypress
            old_x, old_y = self.resize_info
            old_y = oheight - old_y
            o_mag = self.magnitude(old_x, old_y)

            new_mag = self.magnitude(canvas_layout_x, canvas_layout_y)
            self.resize_info = canvas_layout_x, canvas_layout_y
            scale = new_mag / o_mag
            scale = scale * scale
            new_width = int(owidth * scale)
            new_height = int(oheight * scale)
            event.canvas.set_size_request(new_width, new_height)
        else:
            # calc dx = currx - pressx
            widget_x, widget_y = self.canvas_layout.get_pointer()
            self.press = x0, y0, canvas_layout_x, canvas_layout_y
            dx = canvas_layout_x - xpress
            dy = canvas_layout_y - ypress
            new_x = int(round(x0 + dx))
            new_y = int(round(y0 + dy))
            self.canvas_layout.move(event.canvas, new_x, new_y)
            self.press = new_x, new_y, canvas_layout_x, canvas_layout_y

    def magnitude(self, x, y):
        sq1 = x * x
        sq2 = y * y
        return math.sqrt(sq1 + sq2)

    def mouse_on_release(self, event):
        self.press = None
        event.canvas.draw()

    def leave_figure(self, event):
        if (event and event.canvas):
            event.canvas.figure.patch.set_facecolor('white')
            event.canvas.draw()

    def enter_figure(self, event):
        event.canvas.figure.patch.set_facecolor('grey')
        event.canvas.draw()

    def hscale_change(self, range, scroll, value):
        self.sim_manager.current_step = value
        self.update_canvas()

    # Move some of this functionality to the controller
    def step(self):
        self.sim_manager.step()

        self.controller_panel.update_slider(self.sim_manager.min_step, self.sim_manager.last_sim_step,
                                            self.sim_manager.current_step, self.sim_manager.dt)

        if (self.next_gcomponent_redraw == 0):
            self.update_canvas()
            self.next_gcomponent_redraw = self.sim_rate/self.framerate
        else:
            self.next_gcomponent_redraw -= 1

    def draw_ui(self, obj):
        my_figure = obj.get_figure()
        my_ax = obj.get_ax()

        my_ax.add_patch(mpatches.Rectangle((1, 1), 100, 100))
        print (dir(my_ax))


    def update_canvas(self):
        if (self.xy_plot.canvas.get_visible()):
            self.xy_plot.canvas.draw()

    #Controller code for controller_panel
    def format_slider_value(self, scale, value):
        return str(value * self.sim_manager.dt)

    def play_pause_button(self, widget):
        if (self.playing == True):
            self.timer.stop()
            self.playing = False
            self.controller_panel.toggle_play(self.playing)
        else:
            self.timer.start()
            self.playing = True
            self.controller_panel.toggle_play(self.playing)

    def reset_button(self, widget):
        self.timer.stop()
        self.playing = False
        self.controller_panel.toggle_play(self.playing)
        self.sim_manager.reset()
        self.jump_to(widget, self.sim_manager.min_step)
        self.clear_all_graphs()

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

    def show_plot(self, plot):
        plot.canvas.set_visible(True)
        plot.canvas.set_size_request(300, 300)
        self.canvas_layout.put(plot.canvas, 0, 0)

    def remove_plot(self, plot):
        plot.canvas.set_visible(False)
        self.canvas_layout.remove(plot.canvas)

    def toggle_panel(self, widget, panel):
        if (widget.get_active()):
            panel.set_visible(True)
            self.control_panel.add(panel)
        else:
            panel.set_visible(False)
            self.control_panel.remove(panel)

    def clear_all_graphs(self):
        map(lambda x:x.clear(), self.all_plots)

    def repaint_all_canvas(self):
        map(lambda x:x.draw(), self.all_canvas)
