from gi.repository import Gtk

def warning_dialog(parent_widget, text):

    dialog = Gtk.Dialog(title='Aviso',
                        transient_for=parent_widget,
                        flags=0,
                        buttons=(Gtk.STOCK_OK, Gtk.ResponseType.OK))

    label = Gtk.Label(text)
    image = Gtk.Image.new_from_icon_name('dialog-warning', Gtk.IconSize.DIALOG)

    grid = Gtk.Grid()
    grid.set_column_spacing(30)
    grid.attach(image, 0, 0, 1, 1)
    grid.attach_next_to(label, image, Gtk.PositionType.RIGHT, 1, 1)
    grid.set_margin_start(20)
    grid.set_margin_end(20)

    area = dialog.get_content_area()
    area.pack_start(grid, False, False, 15)
    dialog.show_all()
    dialog.run()
    dialog.destroy()
    
