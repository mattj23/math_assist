"""
    This module contains the Expression class, which is a wrapper around the sympy.Expr class that tracks a history
    of operations performed on the expression while mutating the underlying expression value.

"""
from typing import Optional, Dict, List

import sympy
from ._common import MathArg, ToLatex, MathOutput
from ._history import WorkingHistory


def as_expr(item: MathArg) -> sympy.Expr:
    if isinstance(item, Expression):
        return item.expr
    elif isinstance(item, sympy.Expr):
        return item
    else:
        return sympy.Expr(item)


class Expression(ToLatex):
    def __init__(self, expr: sympy.Expr, *args, **kwargs):
        self._expr = expr
        self._history = kwargs.get('history', WorkingHistory())
        self._substitutions = []

    @property
    def history(self) -> WorkingHistory:
        return self._history

    @property
    def expr(self):
        from copy import deepcopy
        return deepcopy(self._expr)

    def to_latex(self) -> str:
        from sympy import latex
        return latex(self._expr)

    def write_history_to(self, output: MathOutput, skip_start_state: bool = False):
        self._history.write_all_to(output, skip_start_state)

    def attach_output(self, output: MathOutput, skip_start_state: bool = False):
        if not skip_start_state:
            output("Initial expression:")
            output(self)
        self._history.attach_output(output)

    def detach_output(self, output: MathOutput):
        self._history.detach_output(output)

    def detach_all_outputs(self):
        self._history.detach_all_outputs()

    def apply(self, sympy_func, *args, description: Optional[str] = None, **kwargs):
        """
        This is a general purpose method to apply a sympy function to the expression. Use this for functions which do
        not already have specific convenience methods implemented in the Expression class.

        If you find yourself needing to use this method, look up the documentation for the sympy function you are
        trying to use to learn what arguments it takes.  The values given in *args and **kwargs will be passed to the
        sympy function unmodified, except for the `description` keyword argument, which will let you add a more
        descriptive message to the history of the expression.  If you don't provide a description, the method name
        will be used as the description.

        This function assumes that the sympy function you are calling takes a sympy.Expr as its first argument and
        returns the updated expression.  If the function you are trying to use does not meet these requirements, you
        will need to write a custom method for the Expression class to wrap the function you are trying to use. You
        also may want to consider using the .expr property to get the sympy.Expr object directly and working with it
        outside the Expression class.

        :param sympy_func: a callable from the sympy library which takes a sympy.Expr as its first argument
        :param args: additional positional arguments to pass to the sympy function
        :param kwargs: additional keyword arguments to pass to the sympy function
        :param description: an optional string to describe the operation in the history
        :return:
        """
        if description is None:
            description = f"Apply '{sympy_func.__name__}'"
        before = self._expr
        after = sympy_func(self._expr, *args, **kwargs)
        self._expr = after
        self._history.append(description, list(args), before=before, after=after)

    def add(self, other: MathArg, description="Add"):
        other = as_expr(other)
        before = self._expr
        self._expr += other
        self._history.append(description, [other], before=before, after=self._expr)

    def subtract(self, other: MathArg, description="Subtract"):
        other = as_expr(other)
        before = self._expr
        self._expr -= other
        self._history.append(description, [other], before=before, after=self._expr)

    def multiply_by(self, other: MathArg, description="Multiply by"):
        other = as_expr(other)
        before = self._expr
        self._expr *= other
        self._history.append(description, [other], before=before, after=self._expr)

    def divide_by(self, other: MathArg, description="Divide by"):
        other = as_expr(other)
        before = self._expr
        self._expr /= other
        self._history.append(description, [other], before=before, after=self._expr)

    def factor(self, deep=False, description="Factor terms"):
        self.apply(sympy.factor, description=description, deep=deep)

    def expand(self, description="Expand terms"):
        self.apply(sympy.expand, description=description)

    def simplify(self, *args, description="Simplify", **kwargs):
        self.apply(sympy.simplify, *args, description=description, **kwargs)

    def collect_coeffs_only(self, terms: List[MathArg]) -> Dict[sympy.Expr, sympy.Expr]:
        """
        Get the coefficients of the expression after the terms have been collected, but without actually doing anything
        to the expression itself.  This does not modify the expression and generates no entry in the history. It is
        the equivalent of calling `sympy.collect` with the `evaluate=False` keyword argument.
        :param terms: the terms to collect, these can be symbols or expressions
        :return: a dictionary of the coefficients of the terms, including the extra constant term 1
        """

        terms = [as_expr(t) for t in terms]
        return self._expr.collect(terms, evaluate=False)

    def collect(self, terms: List[MathArg], description="Collect the terms", **kwargs):
        """
        Collect terms in the expression.  This is the equivalent of calling `sympy.collect` on the expression.
        :param terms: the terms to collect, these can be symbols or expressions
        :param description: an optional string to describe the operation in the history
        """
        terms = [as_expr(t) for t in terms]
        self.apply(sympy.collect, terms, description=description, **kwargs)


    # def substitute(self, *args):
    #     if len(args) == 1 and isinstance(args[0], Equation):
    #         self._substitute(args[0].left, args[0].right)
    #     elif len(args) == 2:
    #         self._substitute(args[0], args[1])
    #     else:
    #         raise ValueError("Invalid arguments for substitution")
    #
    # def _substitute(self, original: Union[Expr, Expression], replacement: Union[Expr, Expression]):
    #     a = _as_expr(original)
    #     b = _as_expr(replacement)
    #     self._expr = self._expr.subs(a, b)
    #     self._history.append("Substituted", a, b)
    #     self._substitutions.append((a, b))
    #
    # def cos(self):
    #     from sympy import cos
    #     self._expr = cos(self._expr)
    #     self._history.append("Applied cosine")
    #
    # def sin(self):
    #     from sympy import sin
    #     self._expr = sin(self._expr)
    #     self._history.append("Applied sine")
    #
    # def tan(self):
    #     from sympy import tan
    #     self._expr = tan(self._expr)
    #     self._history.append("Applied tangent")
    #
    # def acos(self):
    #     from sympy import acos
    #     self._expr = acos(self._expr)
    #     self._history.append("Applied arccosine")
    #
    # def asin(self):
    #     from sympy import asin
    #     self._expr = asin(self._expr)
    #     self._history.append("Applied arcsine")
    #
    # def atan(self):
    #     from sympy import atan
    #     self._expr = atan(self._expr)
    #     self._history.append("Applied arctangent")
    #
    # def to_power(self, power: ValueUnion):
    #     power = _as_expr(power)
    #     self._expr = self._expr ** power
    #     self._history.append("Raised to the power of", power)
    #
    # def as_fraction(self) -> Tuple[Expression, Expression]:
    #     from sympy import fraction
    #     n, d = fraction(self._expr)
    #     return Expression(n), Expression(d)
    #
    # def clone(self):
    #     return deepcopy(self)
