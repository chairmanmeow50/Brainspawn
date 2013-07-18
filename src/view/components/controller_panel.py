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
        self.play_button = gtk.Button(label=None, stock=gtk.STOCK_MEDIA_PLAY)
        self.change_label(self.play_button, "")
        self.play_button.set_size_request(50, 20)
        self.play_button.connect("clicked", main_frame.play_pause_button)
        self.pack_start(self.play_button, False, False, 10)
        self.play_button.show()
        
        self.pause_button = gtk.Button(label=None, stock=gtk.STOCK_MEDIA_PAUSE)
        self.change_label(self.pause_button, "")
        self.pause_button.connect("clicked", main_frame.play_pause_button)
        self.pack_start(self.pause_button, False, False, 10)

        stop_button = gtk.Button(label=None, stock=gtk.STOCK_MEDIA_STOP)
        self.change_label(stop_button, "")
        stop_button.show()
        stop_button.connect("clicked", main_frame.stop_button)
        self.pack_start(stop_button, False, False, 10)
        
        reset_button = gtk.Button("Reset")
        reset_button.show()
        reset_button.connect("clicked", main_frame.reset_button)
        self.pack_start(reset_button, False, False, 10)
        
        jump_front_button = gtk.Button(label=None, stock=gtk.STOCK_MEDIA_PREVIOUS)
        self.change_label(jump_front_button, "")
        jump_front_button.show()
        jump_front_button.connect("clicked", main_frame.jump_to_front)
        self.pack_start(jump_front_button, False, False, 10)
        
        jump_end_button = gtk.Button(label=None, stock=gtk.STOCK_MEDIA_NEXT)
        self.change_label(jump_end_button, "")
        jump_end_button.show()
        jump_end_button.connect("clicked", main_frame.jump_to_end)
        self.pack_start(jump_end_button, False, False, 10)

        self.hscale_adjustment = gtk.Adjustment()
        self.hscale = gtk.HScale(adjustment=self.hscale_adjustment)
        self.add(self.hscale)
        self.hscale.show()
        self.hscale_adjustment.set_lower(0)
        self.hscale_adjustment.set_upper(10)
        self.hscale_adjustment.set_value(self.hscale_adjustment.get_upper())
        self.hscale.connect("change-value", main_frame.hscale_change)

        rate_label = gtk.Label("Rate:")
        rate_label.set_alignment(0, 0.5)
        self.pack_start(rate_label, False, True, 0)
        rate_label.show()

        adj = gtk.Adjustment(1.0, 1.0, 31.0, 1.0, 5.0, 0.0)
        spinner = gtk.SpinButton(adj, 0, 0)
        spinner.set_wrap(True)
        self.pack_start(spinner, False, True, 0)
        spinner.show()
        
    def toggle_play(self, is_playing):
        if (is_playing):
            self.play_button.hide()
            self.pause_button.show()
        else:
            self.play_button.show()
            self.pause_button.hide()
        
    def change_label(self, button, new_label):
        Label=button.get_children()[0]
        Label=Label.get_children()[0].get_children()[1]
        Label=Label.set_label(new_label)
        
    def set_slider(self, value):
        self.hscale.set_value(value)
        
    def update_slider(self, min_tick, max_tick):
        self.hscale_adjustment.set_upper(max_tick)
        self.hscale_adjustment.set_lower(min_tick)
        self.hscale.set_value(max_tick)