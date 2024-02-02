"""
    This module contains the Equation class, which is a wrapper around two Expression objects representing the left
    and right sides of an equation. The Equation class allows operations to be performed independently on the left and
    right expressions, but also provides convenience methods for performing operations on both sides of the equation
    simultaneously, lowering the chance of human error.
"""
from typing import Union, Optional

import sympy
from ._common import MathArg, ToLatex, MathOutput
from ._history import WorkingHistory, IndexSource, ParentHistory
from ._expression import Expression, as_expr


class Equation(ToLatex):

    def to_latex(self) -> str:
        return sympy.latex(self.as_sympy())

    def __init__(self, left: Union[sympy.Expr, sympy.Eq, Expression],
                 right: Optional[MathArg] = None):
        """
        Initialize an equation object with either a single sympy.Eq object, or a left and right side expression either
        as sympy.Expr objects or as Expression objects.  The right side is optional and will be set to 0 if it is not
        provided.

        :param left:
        :param right:
        """

        # We will need a common index source to keep the left and right side histories in sync.
        self._index_source = IndexSource()
        self._history = WorkingHistory(self._index_source, get_combined_state=self.as_sympy)

        self._left_history = WorkingHistory(parent=self._history.as_parent("left side"))
        self._right_history = WorkingHistory(parent=self._history.as_parent("right side"))

        if isinstance(left, sympy.Eq):
            lhs, rhs = left.args
            self._left = Expression(as_expr(lhs), history=self._left_history)
            self._right = Expression(as_expr(rhs), history=self._right_history)
        else:
            self._left = Expression(as_expr(left), history=self._left_history)
            self._right = Expression(as_expr(right or 0), history=self._right_history)

        self._history.update(self.as_sympy())

    def attach_output(self, output: MathOutput, skip_start_state: bool = False):
        if not skip_start_state:
            output("Initial equation:")
            output(self)
        self._history.attach_output(output)

    def detach_output(self, output: MathOutput):
        self._history.detach_output(output)

    def detach_all_outputs(self):
        self._history.detach_all_outputs()

    def as_sympy(self) -> sympy.Eq:
        return sympy.Eq(self._left.expr, self._right.expr)

    @property
    def left(self) -> Expression:
        return self._left

    @property
    def right(self) -> Expression:
        return self._right

    def apply(self, sympy_func, *args, description: Optional[str] = None, **kwargs):
        """
        This is a general purpose method to apply a sympy function to the equation. Use this for functions which do
        not already have specific convenience methods implemented in the Equation class.

        :param sympy_func: The sympy function to apply to the equation.
        :param args: The arguments to pass to the sympy function.
        :param description: A description of the operation to be performed.
        :param kwargs: Any keyword arguments to pass to the sympy function.
        """
        self._left.apply(sympy_func, *args, description=description, **kwargs)
        self._right.apply(sympy_func, *args, description=description, **kwargs)

    def add(self, other: MathArg):
        """ Add the given expression to both sides of the equation. """
        self._left.add(other)
        self._right.add(other)

    def subtract(self, other: MathArg):
        """ Subtract the given expression from both sides of the equation. """
        self._left.subtract(other)
        self._right.subtract(other)

    def multiply_by(self, other: MathArg):
        """ Multiply both sides of the equation by the given expression. """
        self._left.multiply_by(other)
        self._right.multiply_by(other)

    def divide_by(self, other: MathArg):
        """ Divide both sides of the equation by the given expression. """
        self._left.divide_by(other)
        self._right.divide_by(other)

    def factor(self, deep=False):
        """ Factor both sides of the equation. """
        self._left.factor(deep)
        self._right.factor(deep)

    def expand(self):
        """ Expand both sides of the equation. """
        self._left.expand()
        self._right.expand()
