from gi.repository import Gtk

@Gtk.Template(resource_path='/com/github/carlos157oliveira/Calculus/ui/dialogs/about_dialog.ui')
class AboutDialog(Gtk.AboutDialog):
    __gtype_name__ = 'AboutDialog'

    def __init__(self):
        super().__init__()
