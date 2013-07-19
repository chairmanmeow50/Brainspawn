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
        
        self.play_button = self.create_button(gtk.STOCK_MEDIA_PLAY, "clicked", main_frame.play_pause_button)
        self.play_button.show()
        self.pack_start(self.play_button, False, False, 10)
        
        self.pause_button = self.create_button(gtk.STOCK_MEDIA_PAUSE, "clicked", main_frame.play_pause_button)
        self.pack_start(self.pause_button, False, False, 10)

        self.start_label = gtk.Label("0")
        self.start_label.set_alignment(0, 0.5)
        self.start_label.show()
        self.pack_start(self.start_label, False, True, 0)
        
        jump_front_button = self.create_button(gtk.STOCK_MEDIA_PREVIOUS, "clicked", main_frame.jump_to_front)
        jump_front_button.show()
        self.pack_start(jump_front_button, False, False, 10)

        self.hscale_adjustment = gtk.Adjustment()
        self.hscale = gtk.HScale(adjustment=self.hscale_adjustment)
        self.add(self.hscale)
        self.hscale.show()
        self.hscale_adjustment.set_lower(0)
        self.hscale_adjustment.set_upper(10)
        self.hscale_adjustment.set_value(self.hscale_adjustment.get_upper())
        self.hscale.connect("change-value", main_frame.hscale_change)
        
        jump_end_button = self.create_button(gtk.STOCK_MEDIA_NEXT, "clicked", main_frame.jump_to_front)
        jump_end_button.show()
        self.pack_start(jump_end_button, False, False, 10)

        self.end_label = gtk.Label("0")
        self.end_label.set_alignment(0, 0.5)
        self.end_label.show()
        self.pack_start(self.end_label, False, True, 0)
        
        reset_button = self.create_button(gtk.STOCK_UNDO, "clicked", main_frame.reset_button)
        reset_button.show()
        self.pack_start(reset_button, False, False, 10)

        
    def create_button(self, stock, signal, handler):
        button = gtk.Button(label=None)
        image = gtk.Image()
        image.set_from_stock(stock, gtk.ICON_SIZE_BUTTON)
        button.add(image)
        image.show()
        button.props.relief = gtk.RELIEF_NONE
        button.connect(signal, handler)
        return button
    
    def toggle_play(self, is_playing):
        if (is_playing):
            self.play_button.hide()
            self.pause_button.show()
        else:
            self.play_button.show()
            self.pause_button.hide()
        
    def set_slider(self, value):
        self.hscale.set_value(value)
        
    def update_slider(self, min, max):
        self.start_label.set_text(str(min))
        self.end_label.set_text(str(max))
        #self.hscale.set_value(max_tick)