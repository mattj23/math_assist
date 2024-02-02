from __future__ import annotations
from typing import Optional, Union, List, Any, Dict, Callable, Tuple
from dataclasses import dataclass

from sympy import Expr, Eq, solveset
from copy import deepcopy

ValueUnion = Union[int, float, Expr, "Expression"]


def _as_expr(item: Union[Expr, Expression]) -> Expr:
    return item.expr if isinstance(item, Expression) else item


def _as_expression(item: Union[Expr, Expression]) -> Expression:
    return item if isinstance(item, Expression) else Expression(item)


@dataclass
class Step:
    action: str
    arguments: List[Any]


class WorkingHistory:
    def __init__(self, *args, **kwargs):
        self._history: List[Step] = []
        self._on_append: Optional[Callable[[Step], None]] = kwargs.get('on_append', None)

    def append(self, action: str, *args):
        step = Step(action, list(args))
        self._history.append(step)
        if self._on_append:
            self._on_append(step)

    def set_on_append(self, callback: Callable[[Step], None]):
        self._on_append = callback


class Expression:
    def __init__(self, expr: Expr, *args, **kwargs):
        self._expr = expr
        self._history = kwargs.get('history', WorkingHistory())
        self._substitutions = []

    @property
    def history(self) -> WorkingHistory:
        return self._history

    @property
    def expr(self):
        return deepcopy(self._expr)

    def add(self, other: Union[Expr, Expression]):
        other = _as_expr(other)
        self._expr += other
        self._history.append("Added", other)

    def subtract(self, other: Union[Expr, Expression]):
        other = _as_expr(other)
        self._expr -= other
        self._history.append("Subtracted", other)

    def multiply_by(self, other: Union[Expr, Expression]):
        other = _as_expr(other)
        self._expr *= other
        self._history.append("Multiplied by", other)

    def divide_by(self, other: Union[Expr, Expression]):
        other = _as_expr(other)
        self._expr /= other
        self._history.append("Divided by", other)

    def expand(self):
        self._expr = self._expr.expand()
        self._history.append("Expanded")

    def simplify(self):
        self._expr = self._expr.simplify()
        self._history.append("Simplified")

    def factor(self, deep=False):
        self._expr = self._expr.factor(deep=deep)
        self._history.append("Factored")

    def collect(self, variable, evaluate=True) -> Dict[Expr, Expr]:
        result = self._expr.collect(variable, evaluate=False)
        if evaluate:
            self._expr = self._expr.collect(variable)
            self._history.append("Collected", variable)
        return result

    def substitute(self, *args):
        if len(args) == 1 and isinstance(args[0], Equation):
            self._substitute(args[0].left, args[0].right)
        elif len(args) == 2:
            self._substitute(args[0], args[1])
        else:
            raise ValueError("Invalid arguments for substitution")

    def _substitute(self, original: Union[Expr, Expression], replacement: Union[Expr, Expression]):
        a = _as_expr(original)
        b = _as_expr(replacement)
        self._expr = self._expr.subs(a, b)
        self._history.append("Substituted", a, b)
        self._substitutions.append((a, b))

    def cos(self):
        from sympy import cos
        self._expr = cos(self._expr)
        self._history.append("Applied cosine")

    def sin(self):
        from sympy import sin
        self._expr = sin(self._expr)
        self._history.append("Applied sine")

    def tan(self):
        from sympy import tan
        self._expr = tan(self._expr)
        self._history.append("Applied tangent")

    def acos(self):
        from sympy import acos
        self._expr = acos(self._expr)
        self._history.append("Applied arccosine")

    def asin(self):
        from sympy import asin
        self._expr = asin(self._expr)
        self._history.append("Applied arcsine")

    def atan(self):
        from sympy import atan
        self._expr = atan(self._expr)
        self._history.append("Applied arctangent")

    def to_power(self, power: ValueUnion):
        power = _as_expr(power)
        self._expr = self._expr ** power
        self._history.append("Raised to the power of", power)

    def as_fraction(self) -> Tuple[Expression, Expression]:
        from sympy import fraction
        n, d = fraction(self._expr)
        return Expression(n), Expression(d)


    def clone(self):
        return deepcopy(self)


class Equation:
    @staticmethod
    def from_eq(eq: Eq) -> Equation:
        return Equation(*eq.args)

    def __init__(self, left: Union[Expr, Expression], right: Optional[Union[Expr, Expression]] = None):
        self._left = _as_expression(left)
        self._right = _as_expression(right) if right else Expression(Expr(0))
        self._history = WorkingHistory()

        self._left.history.set_on_append(self._left_history)
        self._right.history.set_on_append(self._right_history)

    def _left_history(self, step: Step):
        self._history.append(step.action, step.arguments)

    def _right_history(self, step: Step):
        self._history.append(step.action, step.arguments)

    @property
    def left(self) -> Expression:
        return self._left

    @property
    def right(self) -> Expression:
        return self._right

    @property
    def eq(self):
        return Eq(self._left.expr, self._right.expr)

    def swap_sides(self):
        self._left, self._right = self._right, self._left
        self._left.history.set_on_append(self._left_history)
        self._right.history.set_on_append(self._right_history)

    def add(self, other: Union[Expr, Expression]):
        self._left.add(other)
        self._right.add(other)

    def subtract(self, other: Union[Expr, Expression]):
        self._left.subtract(other)
        self._right.subtract(other)

    def multiply_by(self, other: Union[Expr, Expression]):
        self._left.multiply_by(other)
        self._right.multiply_by(other)

    def divide_by(self, other: Union[Expr, Expression]):
        self._left.divide_by(other)
        self._right.divide_by(other)

    def solve(self, variable, **kwargs):
        return solveset(self.eq, variable, **kwargs)

    def cos(self):
        self._left.cos()
        self._right.cos()

    def sin(self):
        self._left.sin()
        self._right.sin()

    def tan(self):
        self._left.tan()
        self._right.tan()

    def acos(self):
        self._left.acos()
        self._right.acos()

    def asin(self):
        self._left.asin()
        self._right.asin()

    def atan(self):
        self._left.atan()
        self._right.atan()

    def to_power(self, power: ValueUnion):
        self._left.to_power(power)
        self._right.to_power(power)

    def substitute(self, *args):
        self._left.substitute(*args)
        self._right.substitute(*args)

    def clone(self):
        return deepcopy(self)
