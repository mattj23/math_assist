from typing import List

from sympy import Expr, latex
from abc import ABC, abstractmethod
from dataclasses import dataclass
from .._common import ToLatex


@dataclass
class Fragment:
    text: str
    is_latex: bool


def entities_to_fragments(*args) -> List[Fragment]:
    fragments = []
    for arg in args:
        if isinstance(arg, str):
            # Strings are the one thing that we don't convert to latex
            fragments.append(Fragment(arg, False))
        elif isinstance(arg, ToLatex):
            # If it's a ToLatex object, use its to_latex method
            fragments.append(Fragment(arg.to_latex(), True))
        else:
            # For everything else, just convert to latex
            fragments.append(Fragment(latex(arg), True))

    return fragments

