# window.py
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

from gi.repository import Gtk


@Gtk.Template(resource_path='/com/github/carlos157oliveira/Calculus/ui/dialogs/warning_dialog.ui')
class WarningDialog(Gtk.Dialog):
    __gtype_name__ = 'WarningDialog'

    msg = Gtk.Template.Child()


    def __init__(self, parent_widget, **kwargs):

        super().__init__(
            #buttons=(Gtk.STOCK_OK, Gtk.ResponseType.OK),
            transient_for=parent_widget,
            **kwargs)


    def show(self, msg):

        self.msg.set_label(msg)
        self.run()
        self.hide()
