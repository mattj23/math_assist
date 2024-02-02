from ._common import MathOutput
from .._sympy_entities import Expression, Equation
from typing import Optional


class MarkdownOutput(MathOutput):
    def __init__(self, file_name: Optional[str] = None):
        self._lines = []
        self._file_name = file_name

    def __call__(self, *args, **kwargs):
        from sympy import latex
        for arg in args:
            if isinstance(arg, Expression):
                self._write_latex_block(latex(arg.expr))
            elif isinstance(arg, Equation):
                self._write_latex_block(latex(arg.eq))
            elif isinstance(arg, str):
                self._lines.append(arg)
            else:
                self._write_latex_block(latex(arg))

    def _write_latex_block(self, *lines):
        self._lines.append("$$")
        self._lines.extend(lines)
        self._lines.append("$$")

    def get_text(self):
        return "\n".join(self._lines)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._file_name:
            with open(self._file_name, "w") as handle:
                handle.write(self.get_text())
        return False
