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

from gi.repository import Gtk, GLib, Gdk, GdkPixbuf, Gio

from ..utils.plots import Plots
from ..utils.sympy_handler import SympyHandler
from .plot_window import PlotWindow
from .dialogs.warning_dialog import WarningDialog
from .dialogs.about_dialog import AboutDialog

import multiprocessing
import numpy as np

@Gtk.Template(resource_path='/com/github/carlos157oliveira/Calculus/ui/calculus_window.ui')
class CalculusWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'CalculusWindow'

    #resultLabel = Gtk.Template.Child('result')
    operandEntry = Gtk.Template.Child('operand')
    togDiff = Gtk.Template.Child('togDiff')
    togInt = Gtk.Template.Child('togInt')
    variableEntry = Gtk.Template.Child('variable')
    resultImage = Gtk.Template.Child()
    operateSpinner = Gtk.Template.Child()
    sympy_handler = None
    resultColor = None
    operateButton = Gtk.Template.Child()
    plotButton = Gtk.Template.Child()
    menu_button = Gtk.Template.Child()
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        menu_builder = Gtk.Builder.new_from_resource('/com/github/carlos157oliveira/Calculus/ui/menu.ui')
        menu_model = menu_builder.get_object('menu')
        self.menu_button.set_menu_model(menu_model)

        self.add_action_entries([
            ['open_result_in_separate_window', self._open_result_in_separate_window, None, None, None],
            ['copy_result_latex_code', self._copy_result_latex_code, None, None, None],
            ['export_result_as_png', self._export_result_as_png, None, None, None],
            ['open_about_dialog', self._open_about_dialog, None, None, None]
        ])

        self.warning_dialog = WarningDialog(self)
        self.sympy_handler = SympyHandler()

        # getting the style right so the plot of the math formula can be shown accordingly to the theme
        style = self.get_style_context()
        c = style.lookup_color('fg_color')[1]

        # we lock alpha to be equal 1 all the time: we want maximum opacity
        self.resultColor = (c.red, c.green, c.blue, 1)


    def spinner(original_function):
        def modified_function(self, widget):

            def check_function(conn):

                if conn.poll():
                    result = conn.recv()

                    self.operateSpinner.stop()
                    self.operateButton.set_sensitive(True)
                    self.plotButton.set_sensitive(True)

                    # since sympy handler is modified in another process, update it in the main process
                    if result.sympy_handler:
                        self.sympy_handler = result.sympy_handler

                    if result.is_error:
                        self.warning_dialog.show(result.data)
                    else:
                        input_stream = Gio.MemoryInputStream.new_from_data(result.data.getvalue())
                        pixbuf = GdkPixbuf.Pixbuf.new_from_stream(input_stream)
                        self.resultImage.set_from_pixbuf(pixbuf)

                    return False
                else:
                    return True


            self.operateButton.set_sensitive(False)
            self.plotButton.set_sensitive(False)

            self.operateSpinner.start()
            conn1, conn2 = multiprocessing.Pipe(False)
            multiprocessing.Process(target=original_function, args=[self, widget, conn2]).start()
            GLib.timeout_add(250, check_function, conn1)


        return modified_function



    @Gtk.Template.Callback()
    @spinner
    def operate(self, widget, conn):

        variableText = self.variableEntry.get_text()
        operandText = self.operandEntry.get_text()

        if operandText == '':
            conn.send(Result(True, _("Input operand")))
            return

        if variableText == '':
            conn.send(Result(True, _("Input operation variable")))
            return

        try:
            self.sympy_handler.set_variable_from_text(variableText)
            self.sympy_handler.set_operand_from_text(operandText)
        except Exception:
            conn.send(Result(True, _("Syntax error")))
            return

        if(self.togDiff.get_active()):
            self.sympy_handler.diff()
        else:
            self.sympy_handler.integrate()


        txt = self._get_formatted_result()
        try:
            result_data = Plots.get_buffer_with_text(txt, self.resultColor)
        except ValueError:
            conn.send(Result(True, _("Matplotlib is unable to render the output.\nYou can still export the output as LaTeX in the menu."), self.sympy_handler))
            return

        conn.send(Result(False, result_data, self.sympy_handler))


    @Gtk.Template.Callback()
    def invoke_plot_dialog(self, widget):

        if self.sympy_handler.is_result_ready():

            if (self.sympy_handler.is_result_univariable()
                and self.sympy_handler.is_operand_univariable()):

                f = self.sympy_handler.lambdify_operand()
                g = self.sympy_handler.lambdify_result()

                try:
                    # we need to pass numpy arrays because
                    # the inner logic uses a numpy array attribute
                    f(np.array([0]))
                    g(np.array([0]))
                except NameError:
                    self.warning_dialog.show(_("One or more symbols aren't defined"))
                    return
                except ZeroDivisionError:
                    pass

                plot_window = PlotWindow(f1=f, f2=g)
                plot_window.present()
            else:
                self.warning_dialog.show(_("Expressions must be univariable"))

        else:
            self.warning_dialog.show(_("No input data"))


    def _get_formatted_result(self):
        txt = self.sympy_handler.get_last_result_as_latex()
        txt = '{0}{1}{0}'.format('$', txt)
        return txt


    def _open_result_in_separate_window(self, action, param, user_data):

        if not self.sympy_handler.is_result_ready():
            return

        txt = self._get_formatted_result()
        try:
            Plots.open_result_in_external_viewer(txt)
        except ValueError:
            self.warning_dialog.show(_("Matplotlib is unable to render the output.\nYou can still export the output as LaTeX in the menu."))


    def _copy_result_latex_code(self, action, param, user_data):

        self.clipboard.set_text(self.sympy_handler.get_last_result_as_full_latex(), -1)


    def _export_result_as_png(self, action, param, user_data):

        if not self.sympy_handler.is_result_ready():
            return

        file_chooser = Gtk.FileChooserDialog(
            title=_("Export result as PNG"),
            parent=self,
            action=Gtk.FileChooserAction.SAVE,
            do_overwrite_confirmation=True,
            buttons=(
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                Gtk.STOCK_SAVE,
                Gtk.ResponseType.ACCEPT
            )
        )
        file_chooser.set_current_name(_("result.png"))
        response = file_chooser.run()

        try:

            if response == Gtk.ResponseType.ACCEPT:

                filename = file_chooser.get_filename()
                print(filename)
                Plots.save_file_with_result(self._get_formatted_result(), filename)

        except ValueError:
            GLib.idle_add(self.warning_dialog.show, _("Displaying result error"))
        finally:
            file_chooser.destroy()


    def _open_about_dialog(self, action, param, user_data):
        about_dialog = AboutDialog()
        about_dialog.present()


class Result:

    def __init__(self, is_error, data, sympy_handler=None):

        self.is_error = is_error
        self.data = data
        self.sympy_handler = sympy_handler
        
