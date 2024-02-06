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

from ..utils.plots import Plots
from .dialogs.warning_dialog import WarningDialog


@Gtk.Template(resource_path='/com/github/carlos157oliveira/Calculus/ui/plot_window.ui')
class PlotWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'PlotWindow'

    limsupEntry = Gtk.Template.Child()
    liminfEntry = Gtk.Template.Child()
    colorButton1 = Gtk.Template.Child()
    colorButton2 = Gtk.Template.Child()

    def __init__(self, f1, f2, **kwargs):
        super().__init__(**kwargs)

        self.warning_dialog = WarningDialog(self)

        self.f1 = f1
        self.f2 = f2


    @Gtk.Template.Callback()
    def plot(self, widget):

        try:
            limsup = float(self.limsupEntry.get_text())
            liminf = float(self.liminfEntry.get_text())
        except ValueError:
            self.warning_dialog.show(_("The interval must be numeric"))
            return


        color1 = self.colorButton1.get_rgba()
        color2 = self.colorButton2.get_rgba()

        color1 = (color1.red, color1.green, color1.blue)
        color2 = (color2.red, color2.green, color2.blue)

        Plots.n_subplots(_("Original Expression and Result"),
                                (liminf, limsup),
                                (self.f1, self.f2),
                                (_("Original"), _("Result")),
                                (color1, color2))

        self.close()

    @Gtk.Template.Callback()
    def cancel_plot(self, widget):
        self.close()
