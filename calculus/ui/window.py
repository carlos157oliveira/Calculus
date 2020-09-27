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

from ..utils.dialogs import warning_dialog
from ..utils.plots import Plots
from ..utils.sympy_handler import SympyHandler
from .plot_window import PlotWindow

import threading

@Gtk.Template(resource_path='/com/github/carlos157oliveira/Calculus/ui/window.ui')
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


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.sympy_handler = SympyHandler()

        # getting the style right so the plot of the math formula can be shown accordingly to the theme
        style = Gtk.StyleContext()
        c = style.lookup_color('fg_color')[1]
        self.resultColor = (c.red, c.green, c.blue, c.alpha)

    @Gtk.Template.Callback()
    def operate(self, widget):

        thread = threading.Thread(target=self._operate)
        thread.start()


    def spinner(original_function):
        def modified_function(self):
            self.operateSpinner.start()
            original_function(self)
            self.operateSpinner.stop()
        return modified_function

    @spinner
    def _operate(self):

        variableText = self.variableEntry.get_text()
        operandText = self.operandEntry.get_text()

        if variableText == '':
            warning_dialog(self, 'Preencha a variável da operação')
            return

        if operandText == '':
            warning_dialog(self, 'Preencha o operando')
            return

        self.sympy_handler.set_variable_from_text(variableText);
        self.sympy_handler.set_operand_from_text(operandText)

        if(self.togDiff.get_active()):
            self.sympy_handler.diff()
        else:
            self.sympy_handler.integrate()


        txt = self.sympy_handler.get_last_result_as_latex()
        txt = '{0}{1}{0}'.format('$', txt)

        self.resultImage.set_from_pixbuf(Plots.load_pixbuff_text(txt, self.resultColor))

    @Gtk.Template.Callback()
    def invoke_plot_dialog(self, widget):

        if self.sympy_handler.is_result_ready():

            if self.sympy_handler.is_result_univariable():

                f = self.sympy_handler.lambdify_operand()
                g = self.sympy_handler.lambdify_result()

                plot_window = PlotWindow(f1=f, f2=g)
                plot_window.present()
            else:
                warning_dialog(self, 'As expressões devem ser univariável')

        else:
            warning_dialog(self, 'Sem dados de entrada')

