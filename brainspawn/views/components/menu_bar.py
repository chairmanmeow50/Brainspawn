import gtk

class Menu_Bar(gtk.MenuBar):

    def __init__(self, main_frame, controller):
        self.controller = controller
        super(Menu_Bar, self).__init__()

        file_menu = gtk.MenuItem("File")
        file_submenu = gtk.Menu()
        file_menu.set_submenu(file_submenu)

        open_menu_item = gtk.MenuItem("Open Model...")
        open_menu_item.connect("activate", controller.on_open_model)
        open_menu_item.show()
        file_submenu.append(open_menu_item)

        export_pdf_menu_item = gtk.MenuItem("Export to PDF...")
        export_pdf_menu_item.connect('activate', controller.on_export_pdf, main_frame.window)
        export_pdf_menu_item.show()
        file_submenu.append(export_pdf_menu_item)

        file_menu.show()

        self.append (file_menu)
