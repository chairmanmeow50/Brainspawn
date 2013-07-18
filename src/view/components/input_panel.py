import gtk

class Input_Panel(gtk.HBox):
    def __init__(self, main_frame):
        
        super(Input_Panel, self).__init__()
        
        vscale_adjustment = gtk.Adjustment()
        vscale = gtk.VScale(adjustment=vscale_adjustment)
        vscale.show()
        vscale_adjustment.set_lower(0)
        vscale_adjustment.set_upper(10)
        vscale_adjustment.set_value(vscale_adjustment.get_upper())
        #self.vscale_adjustment.connect("value-changed", self.vscale_change)
        
        self.pack_start(vscale, True, False)
        