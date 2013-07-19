#!/usr/bin/env python
import os
import subprocess
import tempfile
from spa_sequence.spa_sequence import net, pThal

import pygtk
pygtk.require('2.0')
import gtk
import cairo

import view.components.spectrogram as spectrogram
#import view.components.input_panel as Input_Panel
from view.components.input_panel import Input_Panel
from view.components.controller_panel import Controller_Panel
from view.components.menu_bar import Menu_Bar
import simulator
import simulator.watchers
from old_plots.xy_plot import XY_Plot
from old_plots.voltage_grid import Voltage_Grid_Plot

from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas

class MainFrame:
    def __init__(self):
        
        self.vbox = gtk.VBox(False, 0)
        self.playing = False

        self.sim = simulator.Simulator(net, net.dt)
        self.sim.add_watcher(simulator.watchers.LFPSpectrogramWatcher())
        self.sim.add_watcher(simulator.watchers.XYWatcher())
        self.sim.add_watcher(simulator.watchers.Voltage_Grid_Watcher())
        self.sim.watcher_manager.add_object("pThal", pThal)
        self.spectrogram = None
        
        self.all_plots = []
        self.all_canvas = []

        net.run(0.001) #run for one timestep
        self.sim.tick()
        self.sim.tick()

        for name, type, data in [("pThal", "LFP Spectrogram", None)]:
            if name in self.sim.watcher_manager.objects.keys():
                for (t, view_class, args) in self.sim.watcher_manager.list_watcher_views(name):
                    if t == type:
                        component = view_class(self.sim, name, **args)
                        # we know we only have the spectrogram in our example
                        self.spectrogram = component
                    elif (t == "XY"):
                        self.xy_plot = view_class(self.sim, name, **args)
                    elif (t == "Voltage Grid"):
                        self.voltage_grid = view_class(self.sim, name, **args)
                        

        self.spec_canvas = FigureCanvas(self.spectrogram.get_figure())
        self.all_plots.append(self.spectrogram)
        self.all_canvas.append(self.spec_canvas)

#         self.xy_plot = XY_Plot()
        self.xy_canvas = FigureCanvas(self.xy_plot.get_figure())
        self.all_plots.append(self.xy_plot)
        self.all_canvas.append(self.xy_canvas)

#         self.voltage_grid = Voltage_Grid_Plot()
        self.vg_canvas = FigureCanvas(self.voltage_grid.get_figure())
        self.all_plots.append(self.voltage_grid)
        self.all_canvas.append(self.vg_canvas)

        # create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_size_request(200, 100)
        self.window.set_title("Nengo Python Visualizer")
        self.window.connect("delete_event", lambda w,e: gtk.main_quit())
        
        self.input_panel = Input_Panel(self)
        self.controller_panel = Controller_Panel(self)
        self.menu_bar = Menu_Bar(self)
        
        self.graph_vbox = gtk.VBox(False, 0)

        figure = self.spectrogram.get_figure()

        self.canvas = FigureCanvas(figure)  # a gtk.DrawingArea
        self.timer = self.canvas.new_timer(interval=200)
        self.timer.add_callback(self.tick)

        self.graph_vbox.pack_start(self.canvas, False, False, 0)

        self.vbox.pack_start(self.menu_bar, False, False, 0)
        self.vbox.pack_start(self.controller_panel, False, False, 0)
        self.vbox.pack_start(self.graph_vbox, False, False, 0)
        self.window.add(self.vbox)
        
        self.menu_bar.show()
        self.controller_panel.show()
        self.spec_canvas.show()
        self.graph_vbox.show()
        self.vbox.show()

        self.window.set_size_request(500, 500)
        self.window.show()
        
        self.menu_bar.spectrogram_menu_item.set_active(True)

    def hscale_change(self, range, scroll, value):
        self.sim.current_tick = value
        self.update_canvas()

    def tick(self):
        self.sim.tick()
        
        self.controller_panel.update_slider(self.sim.min_tick, self.sim.max_tick)
        #self.hscale_adjustment.set_value(self.sim.current_tick) # well, we'll need to find a way to keep this updated at some point

        self.update_canvas()

    def update_canvas(self):

        if (self.xy_canvas.get_visible()):
            self.xy_plot.tick()
            self.xy_canvas.draw()
        if (self.vg_canvas.get_visible()):
            self.voltage_grid.tick()
            self.vg_canvas.draw()
        #self.i=(self.i+1) % 25
        if (self.spec_canvas.get_visible()):
            self.spectrogram.tick()
            self.spec_canvas.draw()


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
        self.clear_all_graphs()
        
    def jump_to_front(self, widget):
        self.jump_to(widget, self.sim.min_tick)
        
    def jump_to(self, widget, value):
        self.playing = True
        self.play_pause_button(widget)
        self.sim.current_tick = value
        self.controller_panel.set_slider(self.sim.current_tick)
        self.update_canvas()
        
    def jump_to_end(self, widget):
        self.jump_to(widget, self.sim.max_tick)

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

    def toggle_plot(self, widget, canvas):
        if (widget.get_active()):
            canvas.set_visible(True)
            self.vbox.add(canvas)
        else:
            canvas.set_visible(False)
            self.vbox.remove(canvas)
            
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
        

    def on_export_pdf(self, widget):
        filename = self.file_browse(gtk.FILE_CHOOSER_ACTION_SAVE,
                                    "screenshot.pdf")
        if filename:
            with open(filename, "wb") as f:
                cr = cairo.Context(cairo.PDFSurface(f, *self.window.get_size()))
                cr.set_source_surface(self.window.window.cairo_create().get_target())
                cr.set_operator(cairo.OPERATOR_SOURCE)
                cr.paint()
                cr.show_page()
                cr.get_target().finish()

    def file_browse(self, action, name="", ext="", ext_name=""):
        if (action == gtk.FILE_CHOOSER_ACTION_OPEN):
            buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                       gtk.STOCK_OPEN, gtk.RESPONSE_OK)
        else:
            buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                       gtk.STOCK_SAVE, gtk.RESPONSE_OK)

        dialog = gtk.FileChooserDialog(title="Select File", action=action,
                                       buttons=buttons)
        dialog.set_current_folder(os.getcwd())
        dialog.set_current_name(name)

        if ext:
            filt = gtk.FileFilter()
            filt.set_name(ext_name if ext_name else ext)
            filt.add_pattern("*." + ext)
            dialog.add_filter(filt)

        filt = gtk.FileFilter()
        filt.set_name("All files")
        filt.add_pattern("*")
        dialog.add_filter(filt)

        result = ""
        if dialog.run() == gtk.RESPONSE_OK:
            result = dialog.get_filename()
        dialog.destroy()
        return result


if __name__ == "__main__":
    MainFrame()
    gtk.main()