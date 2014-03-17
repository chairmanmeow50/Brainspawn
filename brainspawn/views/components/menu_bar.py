import gtk

class Menu_Bar(gtk.MenuBar):

    def __init__(self, main_frame, controller):
        self.controller = controller
        super(Menu_Bar, self).__init__()

        file_menu = gtk.MenuItem("File")
        file_submenu = gtk.Menu()
        file_menu.set_submenu(file_submenu)

        accel = gtk.AccelGroup()
        main_frame.window.add_accel_group(accel)

        open_menu_item = gtk.MenuItem("Open Model...")
        open_menu_item.connect("activate", controller.on_open_model)
        open_menu_item.show()
        file_submenu.append(open_menu_item)

        export_pdf_menu_item = gtk.MenuItem("Export to PDF...")
        export_pdf_menu_item.connect('activate', controller.on_export_pdf, main_frame.window)
        export_pdf_menu_item.show()
        file_submenu.append(export_pdf_menu_item)

        save_menu_item = gtk.MenuItem("Save Layout...")
        save_menu_item.add_accelerator("activate", accel, ord('S'), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        save_menu_item.connect("activate", controller.on_save_layout)
        save_menu_item.show()
        file_submenu.append(save_menu_item)

        open_layout_menu_item = gtk.MenuItem("Restore Layout...")
        open_layout_menu_item.connect("activate", controller.on_restore_layout)
        open_layout_menu_item.show()
        file_submenu.append(open_layout_menu_item)

        file_menu.show()

        self.append (file_menu)
