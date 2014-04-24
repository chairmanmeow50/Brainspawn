""" ResizeBox module, has the ResizeBox class, which 
is a moveable and resizeable Gtk component, used to 
encapsulate plots and give them the ability to be moved
and resized on the visualizer canvas.
"""
import gtk
from gi.repository import Gtk
import settings
from views.network_view import NetworkView
import settings

class ResizeBox(Gtk.EventBox):
    """ ResizeBox class. Inherits from EventBox 
    in order to receive mouse events.
    """

    def __init__(self, plot, canvas_layout):
        """ Initializes resize box. Sets up mouse event handlers.
        """
        super(ResizeBox, self).__init__()
        self._canvas = plot.canvas
        self._plot = plot
        self._canvas_layout = canvas_layout
        self.pos_x = 0
        self.pos_y = 0
        self._is_resize = False
        self._highlight = False
        
        self._drag_begin_x = 0
        self._drag_begin_y = 0
        self._drag = False

        self.add(self._canvas)
        self.set_visible(True)
        self._width = settings.RESIZE_CONTAINER_DEFAULT_WIDTH
        self._height = settings.RESIZE_CONTAINER_DEFAULT_HEIGHT
        self.set_size_request(self.get_width(), self.get_width())
        self._canvas.set_visible(True)

        self.add_events(gtk.gdk.POINTER_MOTION_HINT_MASK)
        self.connect("enter_notify_event", self.enter_notify_handler)
        self.connect("leave_notify_event", self.leave_notify_handler)
        self.connect("button_press_event", self.button_press_handler)
        self.connect("button_release_event", self.button_release_handler)
        self.connect("motion_notify_event", self.motion_notify_handler)
        self.connect("size_allocate", self.size_allocate)

    def button_press_handler(self, widget, event):
        """ When button is pressed, if not the network view,
        bring box to top (z-order). If mouse is pressed within 
        the resize box (bottom right corner), begin resize mode.
        Else, begin move dragging mode.
        """
        if (event.button == 1):
            if not isinstance(self._plot, NetworkView):
                getattr(self.get_window(), 'raise')()
            if (self.is_within_resize_bounds(int(event.x), int(event.y))):
                self._is_resize = True
                self._resize_begin_x, self._resize_begin_y = \
                    self._canvas_layout.get_pointer()
            else:
                self._drag = True
                self._prev_canvas_x, self._prev_canvas_y = \
                    self._canvas_layout.get_pointer()
                self._drag_begin_x = event.x
                self._drag_begin_y = event.y
            self._original_size = self._width, self._height

    def button_release_handler(self, widget, event):
        """ Unset drag and resize flags.
        """
        self._drag = False
        if (self.is_resize()):
            self._is_resize = False

    def motion_notify_handler(self, widget, event):
        """ If in resize mode, calculate size using current mouse 
        coordinates and the position of the resize box. Adjust for 
        the offset difference from clicking within the resize corner.
        There is a minimum width and height.
        
        If in drag mode, calculate offset from current mouse 
        coordinates and previous mouse coordinates.
        """
        if self.is_resize():
            o_width, o_height = self._original_size
            extra_offset_x = o_width - (self._resize_begin_x - self.pos_x)
            extra_offset_y = o_height - (self._resize_begin_y - self.pos_y)
            canvas_x, canvas_y = self._canvas_layout.get_pointer()
            new_width = canvas_x - self.pos_x + extra_offset_x
            new_height = canvas_y - self.pos_y + extra_offset_y
            new_width = max(new_width, settings.RESIZE_MIN_WIDTH)
            new_height = max(new_height, settings.RESIZE_MIN_HEIGHT)
            self.set_size(new_width, new_height)
        elif self._drag:
            canvas_x, canvas_y = self._canvas_layout.get_pointer()
            offset_x = canvas_x - self._prev_canvas_x
            offset_y = canvas_y - self._prev_canvas_y
            new_x = int(round(self.pos_x + offset_x))
            new_y = int(round(self.pos_y + offset_y))
            self.set_position(new_x, new_y)
            self._prev_canvas_x = canvas_x
            self._prev_canvas_y = canvas_y

    def size_allocate(self, widget, allocation):
        """ Resize the actual canvas within the resize box 
        to a size based on the width of border.
        """
        border_width = settings.RESIZE_BOX_WIDTH + \
            settings.RESIZE_BOX_LINE_WIDTH
        allocation.x = border_width
        allocation.y = border_width
        allocation.width = allocation.width - border_width * 2
        allocation.height = allocation.height - border_width * 2
        self._canvas.size_allocate(allocation)
        self._canvas.figure.tight_layout()

    def get_canvas(self):
        """ Returns the canvas object.
        """
        return self._canvas

    def get_canvas_layout(self):
        """ Returns the canvas layout this resize box
        is located.
        """
        return self._canvas_layout

    def get_width(self):
        """ Returns width.
        """
        return self._width

    def get_height(self):
        """ Returns height.
        """
        return self._height

    def leave_notify_handler(self, widget, event):
        """ If mouse leaves event box, turn off highlighting.
        Queus a draw after turning highlighting off.
        """
        if (self.is_resize()):
            return
        if (event.detail != gtk.gdk.NOTIFY_INFERIOR):
            self._highlight = False
            self.queue_draw()

    def do_draw(self, ctx):
        """ If resize box is highlighted, draw a dashed border 
        around the box.
        
        Also draws the resize box corner (mouse presses in corner
        resize the box).
        """
        if (self._highlight):
            # selection box
            ctx.new_path()
            ctx.set_line_width(1)
            ctx.rectangle(0, 0, self.get_width(), self.get_height())
            ctx.set_source_rgba(0, 0, 0, 1)
            ctx.set_dash([5, 10], 2)
            ctx.stroke()

            # resize box
            ctx.new_path()
            ctx.set_line_width(settings.RESIZE_BOX_LINE_WIDTH)
            bottom_right_x = self.get_width() - \
                settings.RESIZE_BOX_WIDTH - settings.RESIZE_BOX_LINE_WIDTH / 2
            bottom_right_y = self.get_height() - \
                settings.RESIZE_BOX_HEIGHT - settings.RESIZE_BOX_LINE_WIDTH / 2
            ctx.rectangle(bottom_right_x, bottom_right_y, 
                          settings.RESIZE_BOX_WIDTH, settings.RESIZE_BOX_HEIGHT)
            ctx.set_source_rgba(0, 0, 0, 1)
            ctx.set_dash([], 0)
            ctx.stroke()

        self.propagate_draw(self._canvas, ctx)

    def enter_notify_handler(self, widget, event):
        """ When mouse is in resize box, highlight it.
        """
        self._highlight = True
        self.queue_draw()

    def is_within_resize_bounds(self, x, y):
        """ Checks if mouse is inside the resize box corner.
        """
        x_min = self.get_width() - \
            settings.RESIZE_BOX_WIDTH - \
            settings.RESIZE_BOX_LINE_WIDTH / 2
        y_min = self.get_height() - \
            settings.RESIZE_BOX_HEIGHT - \
            settings.RESIZE_BOX_LINE_WIDTH / 2
        x_max = x_min + settings.RESIZE_BOX_WIDTH + \
            settings.RESIZE_BOX_LINE_WIDTH / 2
        y_max = y_min + settings.RESIZE_BOX_HEIGHT + \
            settings.RESIZE_BOX_LINE_WIDTH / 2
        if (x >= x_min and x <= x_max and y >= y_min and y <= y_max):
            return True
        return False

    def is_resize(self):
        """ Checks if in resize mode.
        """
        return self._is_resize

    def set_position(self, new_x, new_y):
        """ Sets position to new position, then tells canvas 
        to move the actual resize box to new position.
        """
        self.pos_x = new_x
        self.pos_y = new_y
        self._canvas_layout.move(self, self.pos_x, self.pos_y)

    def set_size(self, new_width, new_height):
        """ Sets size to new size, then makes a call to
        set_size_reqest to resize the resize box.
        
        Calls tight_layout to improve text layout in plot.
        """
        self._width = new_width
        self._height = new_height
        self.set_size_request(self._width, self._height)
        self._canvas.figure.tight_layout()

