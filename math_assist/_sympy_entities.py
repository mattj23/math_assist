# from __future__ import annotations
# from typing import Optional, Union, List, Any, Dict, Callable, Tuple
# from dataclasses import dataclass
#
# from sympy import Expr, Eq, solveset
# from copy import deepcopy
#
# ValueUnion = Union[int, float, Expr, "Expression"]
#
#
# def _as_expr(item: Union[Expr, Expression]) -> Expr:
#     return item.expr if isinstance(item, Expression) else item
#
#
# def _as_expression(item: Union[Expr, Expression]) -> Expression:
#     return item if isinstance(item, Expression) else Expression(item)
#
#
# @dataclass
# class Step:
#     action: str
#     arguments: List[Any]
#
#
# class WorkingHistory:
#     def __init__(self, *args, **kwargs):
#         self._history: List[Step] = []
#         self._on_append: Optional[Callable[[Step], None]] = kwargs.get('on_append', None)
#
#     def append(self, action: str, *args):
#         step = Step(action, list(args))
#         self._history.append(step)
#         if self._on_append:
#             self._on_append(step)
#
#     def set_on_append(self, callback: Callable[[Step], None]):
#         self._on_append = callback
#
#
#
# class Equation:
#     @staticmethod
#     def from_eq(eq: Eq) -> Equation:
#         return Equation(*eq.args)
#
#     def __init__(self, left: Union[Expr, Expression], right: Optional[Union[Expr, Expression]] = None):
#         self._left = _as_expression(left)
#         self._right = _as_expression(right) if right else Expression(Expr(0))
#         self._history = WorkingHistory()
#
#         self._left.history.set_on_append(self._left_history)
#         self._right.history.set_on_append(self._right_history)
#
#     def _left_history(self, step: Step):
#         self._history.append(step.action, step.arguments)
#
#     def _right_history(self, step: Step):
#         self._history.append(step.action, step.arguments)
#
#     @property
#     def left(self) -> Expression:
#         return self._left
#
#     @property
#     def right(self) -> Expression:
#         return self._right
#
#     @property
#     def eq(self):
#         return Eq(self._left.expr, self._right.expr)
#
#     def swap_sides(self):
#         self._left, self._right = self._right, self._left
#         self._left.history.set_on_append(self._left_history)
#         self._right.history.set_on_append(self._right_history)
#
#     def add(self, other: Union[Expr, Expression]):
#         self._left.add(other)
#         self._right.add(other)
#
#     def subtract(self, other: Union[Expr, Expression]):
#         self._left.subtract(other)
#         self._right.subtract(other)
#
#     def multiply_by(self, other: Union[Expr, Expression]):
#         self._left.multiply_by(other)
#         self._right.multiply_by(other)
#
#     def divide_by(self, other: Union[Expr, Expression]):
#         self._left.divide_by(other)
#         self._right.divide_by(other)
#
#     def solve(self, variable, **kwargs):
#         return solveset(self.eq, variable, **kwargs)
#
#     def cos(self):
#         self._left.cos()
#         self._right.cos()
#
#     def sin(self):
#         self._left.sin()
#         self._right.sin()
#
#     def tan(self):
#         self._left.tan()
#         self._right.tan()
#
#     def acos(self):
#         self._left.acos()
#         self._right.acos()
#
#     def asin(self):
#         self._left.asin()
#         self._right.asin()
#
#     def atan(self):
#         self._left.atan()
#         self._right.atan()
#
#     def to_power(self, power: ValueUnion):
#         self._left.to_power(power)
#         self._right.to_power(power)
#
#     def substitute(self, *args):
#         self._left.substitute(*args)
#         self._right.substitute(*args)
#
#     def clone(self):
#         return deepcopy(self)
