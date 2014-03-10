import gtk
from gi.repository import Gtk
import settings
import math

class ResizeBox(gtk.EventBox):
    
    def __init__(self, canvas, canvas_layout):
        super(ResizeBox, self).__init__()
        self._canvas = canvas
        self._canvas_layout = canvas_layout
        self._press = None
        self._resize_info = None
        self._pos_x = 0
        self._pos_y = 0
        self._is_resize = False
        self._highlight = False
        
        self.add(self._canvas)
        self.set_visible(True)
        self._width = settings.RESIZE_CONTAINER_DEFAULT_WIDTH
        self._height = settings.RESIZE_CONTAINER_DEFAULT_HEIGHT
        self.set_size_request(self.get_width(), self.get_width())
        self._canvas.set_visible(True)
        
        self.connect("enter_notify_event", self.enter_notify_handler)
        self.connect("leave_notify_event", self.leave_notify_handler)
        self.connect("button_press_event", self.button_press_handler)
        self.connect("button_release_event", self.button_release_handler)
        self.connect("motion_notify_event", self.motion_notify_handler)
        
    def get_canvas(self):
        return self._canvas
    
    def get_canvas_layout(self):
        return self._canvas_layout
    
    def get_width(self):
        return self._width
    
    def get_height(self):
        return self._height
    
    def leave_notify_handler(self, widget, event):
        self._canvas.draw()
    
    def draw_selection(self):
        ctx = self._canvas.get_property('window').cairo_create()
        
        # selection box
        ctx.new_path()
        ctx.set_line_width(1)
        ctx.rectangle(0, 0, self.get_width(), self.get_height())
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_dash([5, 10], 2)
        ctx.stroke()
        
        # resize box
        ctx.new_path()
        ctx.set_line_width(settings.RESIZE_BOX_LINE_WIDTH)
        bottom_right_x = self.get_width() - settings.RESIZE_BOX_WIDTH - settings.RESIZE_BOX_LINE_WIDTH / 2
        bottom_right_y = self.get_height() - settings.RESIZE_BOX_HEIGHT - settings.RESIZE_BOX_LINE_WIDTH / 2
        ctx.rectangle(bottom_right_x, bottom_right_y, settings.RESIZE_BOX_WIDTH, settings.RESIZE_BOX_HEIGHT)
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_dash([], 0)
        ctx.stroke()
        
        #resize plus
        ctx.new_path()
        resize_box_plus_y_start = bottom_right_y + (settings.RESIZE_BOX_HEIGHT - settings.RESIZE_BOX_PLUS_LENGTH) / 2
        ctx.move_to(bottom_right_x + settings.RESIZE_BOX_WIDTH / 2, resize_box_plus_y_start)
        ctx.line_to(bottom_right_x + settings.RESIZE_BOX_WIDTH / 2, resize_box_plus_y_start + settings.RESIZE_BOX_PLUS_LENGTH)
        ctx.stroke()
        
        ctx.new_path()
        resize_box_plus_x_start = bottom_right_x + (settings.RESIZE_BOX_WIDTH - settings.RESIZE_BOX_PLUS_LENGTH) / 2
        ctx.move_to(resize_box_plus_x_start, bottom_right_y + settings.RESIZE_BOX_HEIGHT / 2)
        ctx.line_to(resize_box_plus_x_start + settings.RESIZE_BOX_PLUS_LENGTH, bottom_right_y + settings.RESIZE_BOX_HEIGHT / 2)
        ctx.stroke()
    
    def enter_notify_handler(self, widget, event):
        self._highlight = True
        self.draw_selection()
        
    def is_within_resize_bounds(self, x, y):
        x_min = self.get_width() - settings.RESIZE_BOX_WIDTH - settings.RESIZE_BOX_LINE_WIDTH / 2
        y_min = self.get_height() - settings.RESIZE_BOX_HEIGHT - settings.RESIZE_BOX_LINE_WIDTH / 2
        x_max = x_min + settings.RESIZE_BOX_WIDTH + settings.RESIZE_BOX_LINE_WIDTH / 2
        y_max = y_min + settings.RESIZE_BOX_HEIGHT + settings.RESIZE_BOX_LINE_WIDTH / 2
        if (x >= x_min and x <= x_max and y >= y_min and y <= y_max):
            return True
        return False

    def is_resize(self):
        return self._is_resize

    def button_press_handler(self, widget, event):
        if (event.button == 1):
            x0 = self._canvas_layout.child_get_property(self, "x")
            y0 = self._canvas_layout.child_get_property(self, "y")
            widget_x, widget_y = self._canvas_layout.get_pointer()
            if (self.is_within_resize_bounds(widget_x - self._pos_x, widget_y - self._pos_y)):
                self._is_resize = True
            self._press = x0, y0, widget_x, widget_y
        
    def button_release_handler(self, widget, event):
        self._press = None
        if (self.is_resize()):
            self._is_resize = False
        self._canvas.draw()
        if (self._highlight):
            self.draw_selection()
        
    def motion_notify_handler(self, widget, event):
        if self._press is None: return
        
        x0, y0, xpress, ypress = self._press
        canvas_layout_x, canvas_layout_y = self._canvas_layout.get_pointer()
        
        widget_x = canvas_layout_x - self._pos_x
        widget_y = canvas_layout_y - self._pos_y
        if (self.is_resize()):
            self._width = canvas_layout_x - self._pos_x
            self._height = canvas_layout_y - self._pos_y
            self.set_size_request(self._width, self._height)
            
        else:
            widget_x, widget_y = self._canvas_layout.get_pointer()
            self._press = x0, y0, widget_x, widget_y
            dx = widget_x - xpress
            dy = widget_y - ypress
            new_x = int(round(x0 + dx))
            new_y = int(round(y0 + dy))
            self._pos_x = new_x
            self._pos_y = new_y
            self._canvas_layout.move(self, self._pos_x, self._pos_y)
            self._press = new_x, new_y, widget_x, widget_y
        
        self.draw_selection()
