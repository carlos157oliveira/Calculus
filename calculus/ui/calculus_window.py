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

from gi.repository import Gtk, GLib

from ..utils.plots import Plots
from ..utils.sympy_handler import SympyHandler
from .plot_window import PlotWindow
from .dialogs.warning_dialog import WarningDialog

import threading
from queue import Queue
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


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.warning_dialog = WarningDialog(self)
        self.sympy_handler = SympyHandler()

        # getting the style right so the plot of the math formula can be shown accordingly to the theme
        style = self.get_style_context()
        c = style.lookup_color('fg_color')[1]

        # we lock alpha to be equal 1 all the time: we want maximum opacity
        self.resultColor = (c.red, c.green, c.blue, 1)


    def spinner(original_function):
        def modified_function(self, widget):

            def check_function(q):
                if not q.empty():
                    error = q.get()
                    self.operateSpinner.stop()
                    self.operateButton.set_sensitive(True)
                    self.plotButton.set_sensitive(True)
                    if error:
                        self.warning_dialog.show(error)
                    q.task_done()
                    return False
                return True

            self.operateButton.set_sensitive(False)
            self.plotButton.set_sensitive(False)


            self.operateSpinner.start()
            q = Queue()
            threading.Thread(target=original_function, args=[self, widget, q]).start()
            GLib.timeout_add(250, check_function, q)


        return modified_function



    @Gtk.Template.Callback()
    @spinner
    def operate(self, widget, q):


        variableText = self.variableEntry.get_text()
        operandText = self.operandEntry.get_text()

        if operandText == '':
            q.put(_('Input operand'))
            return

        if variableText == '':
            q.put(_('Input operation variable'))
            return

        try:
            self.sympy_handler.set_variable_from_text(variableText)
            self.sympy_handler.set_operand_from_text(operandText)
        except Exception:
            q.put(_('Syntax error'))
            return

        if(self.togDiff.get_active()):
            self.sympy_handler.diff()
        else:
            self.sympy_handler.integrate()


        txt = self.sympy_handler.get_last_result_as_latex()
        txt = '{0}{1}{0}'.format('$', txt)
        try:
            self.resultImage.set_from_pixbuf(Plots.load_pixbuff_text(txt, self.resultColor))
        except ValueError:
            q.put(_('Displaying result error'))
            return

        q.put(None)


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
                    self.warning_dialog.show(_('One or more symbols aren\'t defined'))
                    return
                except ZeroDivisionError:
                    pass

                plot_window = PlotWindow(f1=f, f2=g)
                plot_window.present()
            else:
                self.warning_dialog.show(_('Expressions must be univariable'))

        else:
            self.warning_dialog.show(_('No input data'))

