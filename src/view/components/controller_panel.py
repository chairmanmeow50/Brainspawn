'''
Created on Jul 18, 2013

@author: vagrant
'''
import gtk

class Controller_Panel(gtk.HBox):
    '''
    classdocs
    '''


    def __init__(self, main_frame):
        '''
        Constructor
        '''
        
        super(Controller_Panel, self).__init__(False, 10)
        #controller_hbox = gtk.HBox(False, 10)
        self.set_size_request(300, 50)
        play_button = gtk.Button("Play")
        play_button.set_size_request(50, 20)
        play_button.connect("clicked", main_frame.play_pause_button)

        self.pack_start(play_button, False, False, 10)
        play_button.show()

        stop_button = gtk.Button("Stop")
        stop_button.show()
        stop_button.connect("clicked", main_frame.stop_button)
        self.pack_start(stop_button, False, False, 10)

        self.hscale_adjustment = gtk.Adjustment()
        hscale = gtk.HScale(adjustment=self.hscale_adjustment)
        self.add(hscale)
        hscale.show()
        self.hscale_adjustment.set_lower(0)
        self.hscale_adjustment.set_upper(10)
        self.hscale_adjustment.set_value(self.hscale_adjustment.get_upper())
        self.hscale_adjustment.connect("value-changed", main_frame.hscale_change)

        rate_label = gtk.Label("Rate:")
        rate_label.set_alignment(0, 0.5)
        self.pack_start(rate_label, False, True, 0)
        rate_label.show()

        adj = gtk.Adjustment(1.0, 1.0, 31.0, 1.0, 5.0, 0.0)
        spinner = gtk.SpinButton(adj, 0, 0)
        spinner.set_wrap(True)
        self.pack_start(spinner, False, True, 0)
        spinner.show()