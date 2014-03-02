""" Abstract base class for Visualizations
"""

import gtk
from abc import ABCMeta, abstractmethod
from matplotlib.backends.backend_gtkcairo import FigureCanvasGTKCairo as FigureCanvas

class Visualization(object):
    """Visualization class
    """

    __metaclass__ = ABCMeta

    @property
    def figure(self):
        return self._figure

    @property
    def canvas(self):
        return self._canvas

    @abstractmethod
    def update(self, data, start_time):
        """ Callback function passed to observer nodes
        """
        pass

    @abstractmethod
    def clear(self):
        """ Clear the graph
        """
        pass

    def init_canvas(self, figure):
        self._canvas = FigureCanvas(figure)
        self._canvas.connect("event", self.button_press, self._canvas)

    def button_press(self, widget, event, canvas):
        if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
            export_pdf_item = gtk.MenuItem("Export to PDF")
            export_pdf_item.connect("activate", self.on_export_pdf, canvas)
            export_pdf_item.show()
            context_menu = gtk.Menu()
            context_menu.append(export_pdf_item)
            context_menu.popup(None, None, None, event.button, event.time)
            return True
        return False

    def on_export_pdf(self, widget, canvas=None):
        filename = self.file_browse(gtk.FILE_CHOOSER_ACTION_SAVE, "screenshot.pdf")
        if not filename:
            return
        with open(filename, "wb") as f:
            if canvas:
                canvas.print_pdf(f)
            else:
                cr = cairo.Context(cairo.PDFSurface(f, *self.window.get_size()))
                cr.set_source_surface(self.window.window.cairo_create().get_target())
                cr.set_operator(cairo.OPERATOR_SOURCE)
                cr.paint()
                cr.show_page()
                cr.get_target().finish()

    def file_browse(self, action, name="", ext="", ext_name=""):
        if (action == gtk.FILE_CHOOSER_ACTION_OPEN):
            buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK)
        else:
            buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK)
        dialog = gtk.FileChooserDialog(title="Select File", action=action, buttons=buttons)
        dialog.set_do_overwrite_confirmation(True)
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


