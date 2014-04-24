""" Module for file menu bar in visualizer.
"""

import gtk


class Menu_Bar(gtk.MenuBar):
    """ Custom menu bar class called Menu_Bar.
    """

    def __init__(self, main_frame, controller):
        """ Initializes menu bar.

        Adds file menu with items: open model and
        export to pdf.
        """
        self.controller = controller
        super(Menu_Bar, self).__init__()

        file_menu = gtk.MenuItem("File")
        file_submenu = gtk.Menu()
        file_menu.set_submenu(file_submenu)

        accel = gtk.AccelGroup()
        main_frame.window.add_accel_group(accel)

        open_menu_item = gtk.MenuItem("Open Model...")
        open_menu_item.add_accelerator("activate", accel, ord('O'),
                                       gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        open_menu_item.connect("activate", controller.on_open_model)
        open_menu_item.show()
        file_submenu.append(open_menu_item)

        export_pdf_menu_item = gtk.MenuItem("Export to PDF...")
        export_pdf_menu_item.connect('activate', controller.on_export_pdf,
                                     main_frame.window)
        export_pdf_menu_item.show()
        file_submenu.append(export_pdf_menu_item)

        file_menu.show()

        self.append(file_menu)
