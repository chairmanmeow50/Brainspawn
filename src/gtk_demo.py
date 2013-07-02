#!/usr/bin/env python
from spa_sequence.spa_sequence import net, pThal

import pygtk
pygtk.require('2.0')
import gtk

import view.components.spectrogram as spectrogram
import simulator
import simulator.watchers
from old_plots.xy_plot import XY_Plot
from old_plots.voltage_grid import Voltage_Grid_Plot

from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas

class MenuExample:
    def __init__(self):
        self.playing = False
        
        self.sim = simulator.Simulator(net, net.dt)
        self.sim.add_watcher(simulator.watchers.LFPSpectrogramWatcher())
        self.sim.watcher_manager.add_object("pThal", pThal)
        self.spectrogram = None

        net.run(0.001) #run for one timestep
        
        for name, type, data in [("pThal", "LFP Spectrogram", None)]:
            if name in self.sim.watcher_manager.objects.keys():
                for (t, view_class, args) in self.sim.watcher_manager.list_watcher_views(name):
                    if t == type:
                        component = view_class(self.sim, name, **args)
                        # we know we only have the spectrogram in our example
                        self.spectrogram = component
        
        self.spec_canvas = FigureCanvas(self.spectrogram.get_figure())
        
        self.xy_plot = XY_Plot()
        self.xy_canvas = FigureCanvas(self.xy_plot.get_figure())
        self.i=0
        
        self.voltage_grid = Voltage_Grid_Plot()
        self.vg_canvas = FigureCanvas(self.voltage_grid.get_figure())
        
        # create a new window
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_size_request(200, 100)
        window.set_title("Nengo Python Visualizer")
        window.connect("delete_event", lambda w,e: gtk.main_quit())
        
        menu = gtk.Menu()

        file_menu = gtk.MenuItem("File")

        file_menu.show()

        file_menu.set_submenu(menu)

        tools_menu = gtk.MenuItem("Tools")
        tools_menu.show()

        view_menu = gtk.MenuItem("View")
        view_submenu = gtk.Menu()
        view_menu.set_submenu(view_submenu)
        
        spectrogram_menu_item = gtk.CheckMenuItem("Spectrogram")
        spectrogram_menu_item.connect("activate", self.toggle_plot, self.spec_canvas)
        spectrogram_menu_item.set_active(True)
        spectrogram_menu_item.show()
        view_submenu.append(spectrogram_menu_item)
        
        xy_plot_menu_item = gtk.CheckMenuItem("XY plot") 
        xy_plot_menu_item.connect("activate", self.toggle_plot, self.xy_canvas)
        xy_plot_menu_item.show()
        view_submenu.append(xy_plot_menu_item)
        
        voltage_grid_menu_item = gtk.CheckMenuItem("Voltage Grid")
        voltage_grid_menu_item.connect("activate", self.toggle_plot, self.vg_canvas)
        voltage_grid_menu_item.show()
        view_submenu.append(voltage_grid_menu_item)
        
        view_menu.show()

        help_menu = gtk.MenuItem("Help")
        help_menu.show()

        self.vbox = gtk.VBox(False, 0)
        window.add(self.vbox)
        self.vbox.show()

        menu_bar = gtk.MenuBar()
        menu_bar.show()
        menu_bar.set_size_request(300, 30)
        
        menu_bar.append (file_menu)
        menu_bar.append (tools_menu)
        menu_bar.append (view_menu)
        menu_bar.append (help_menu)
        self.vbox.pack_start(menu_bar, False, False, 2)

        frame = gtk.Frame(label="Spectrogram")
        frame.set_size_request(300, 300)

        figure = self.spectrogram.get_figure()
 
        self.canvas = FigureCanvas(figure)  # a gtk.DrawingArea
        self.timer = self.canvas.new_timer(interval=100)
        self.timer.add_callback(self.update_canvas)
        self.spec_canvas.show()

        controller_hbox = gtk.HBox(False, 10)
        controller_hbox.set_size_request(300, 50)
        play_button = gtk.Button("Play")
        play_button.set_size_request(50, 20)
        play_button.connect("clicked", self.play_pause_button)
        
        controller_hbox.pack_start(play_button, False, False, 10)
        play_button.show()
        
        stop_button = gtk.Button("Stop")
        stop_button.show()
        stop_button.connect("clicked", self.stop_button)
        controller_hbox.pack_start(stop_button, False, False, 10)

        hscale = gtk.HScale(adjustment=None)
        controller_hbox.add(hscale)
        hscale.show()

        rate_label = gtk.Label("Rate:")
        rate_label.set_alignment(0, 0.5)
        controller_hbox.pack_start(rate_label, False, True, 0)
        rate_label.show()
   
        adj = gtk.Adjustment(1.0, 1.0, 31.0, 1.0, 5.0, 0.0)
        spinner = gtk.SpinButton(adj, 0, 0)
        spinner.set_wrap(True)
        controller_hbox.pack_start(spinner, False, True, 0)
        spinner.show()
        
        self.vbox.pack_start(controller_hbox, False, False, 0)
        controller_hbox.set_size_request(300, 50)
        controller_hbox.show()
        
        self.vbox.add(self.spec_canvas) 
        

        window.set_size_request(500, 500)
        window.show()

    def update_canvas(self):
        self.sim.tick()
        
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
        else:
            self.timer.start()
            self.playing = True

    def stop_button(self, widget):
        self.timer.stop()
        self.playing = False

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

if __name__ == "__main__":
    MenuExample()
    gtk.main()
