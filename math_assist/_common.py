from sympy import Expr
from typing import Optional, Union, List, Any, Dict, Callable, Tuple
from abc import ABC, abstractmethod
from uuid import UUID, uuid4

MathArg = Union[int, float, "Expression", Expr]


class ToLatex(ABC):
    @abstractmethod
    def to_latex(self) -> str:
        pass


class MathOutput(ABC):
    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_text(self):
        pass
