import gtk

class Input_Panel(gtk.HBox):
    def __init__(self):
        
        self.vscale_adjustment = gtk.Adjustment()
        vscale = gtk.VScale(adjustment=self.vscale_adjustment)
        vscale.show()
        self.vscale_adjustment.set_lower(0)
        self.vscale_adjustment.set_upper(10)
        self.vscale_adjustment.set_value(self.vscale_adjustment.get_upper())
        #self.vscale_adjustment.connect("value-changed", self.vscale_change)
        
        #self.pack_start(vscale, True, False)
        