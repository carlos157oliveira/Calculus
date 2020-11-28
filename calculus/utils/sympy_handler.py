import sympy
import numpy as np
import re
#import svgmath
#from sympy.utilities.mathml import c2p

class SympyHandler:

    variable = None
    operand = None
    last_result = None
    '''
    patterns = (
        (re.compile(r'\\begin{\w*}|\\end{\w*}'), r''),
        (re.compile(r'\\text{(\w*)}'), r'\1'),
        (re.compile(r'\\\\'), r'&')
        )
    '''
    patterns = (
        (re.compile(r'\\begin{\w*}|\\end{\w*}'), r''),
        (re.compile(r'\\text{(\w*)}'), r'\1')
    )


    def set_variable_from_text(self, variableText):
        self.variable = sympy.Symbol(variableText)


    def set_operand_from_text(self, operandText):
        operand = sympy.sympify(operandText)

        # adequate euler number for sympy library
        self.operand = operand.subs('e', 'E')


    def diff(self):
        self.last_result = self.operand.diff(self.variable)
        return self.last_result


    def integrate(self):
        self.last_result = self.operand.integrate(self.variable)
        return self.last_result


    def get_last_result(self):
        return self.last_result


    def get_last_result_as_latex(self):

        txt = sympy.latex(self.last_result)
        for p in self.patterns:
            txt = p[0].sub(p[1], txt)

        indexFound = txt.find('&')
        if indexFound != -1:
            txt = txt[:indexFound]

        return txt


    def get_last_result_as_full_latex(self):
        if self.last_result:
            return sympy.latex(self.last_result)
        else:
            return ''


    def is_result_ready(self):
        return self.last_result is not None


    def lambdify(self, expr):
        if expr.is_constant():
            return lambda x: np.full(x.shape[0], expr)
        else:
            return sympy.lambdify(self.variable, expr, 'numpy')


    def lambdify_operand(self):
        return self.lambdify(self.operand)


    def lambdify_result(self):
        return self.lambdify(self.last_result)


    def is_result_univariable(self):
        return len(self.last_result.free_symbols) <= 1


    def is_operand_univariable(self):
        return len(self.operand.free_symbols) <= 1

