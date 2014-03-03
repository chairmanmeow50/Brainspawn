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

        tools_menu = gtk.MenuItem("Tools")
        tools_submenu = gtk.Menu()
        tools_menu.set_submenu(tools_submenu)

        resize_menu_item = gtk.CheckMenuItem("Resize")
        resize_menu_item.connect("activate", main_frame.toggle_resize)
        tools_submenu.append(resize_menu_item)

        tools_menu.show()

        self.append (file_menu)
        self.append (tools_menu)
