# main.py
#
# Copyright 2020 ceo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys, os
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gio, Gdk

from .ui.window import CalculusWindow


class Application(Gtk.Application):

    def __init__(self):
        super().__init__(application_id='org.example.App',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

        base_path = '/org/example/App'

        self.props.resource_base_path = base_path

        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource(os.path.join(base_path, 'style.css'))
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = CalculusWindow(application=self)
        win.present()


def main(version):
    app = Application()
    return app.run(sys.argv)
