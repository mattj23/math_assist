from .._common import MathOutput
from ._common import entities_to_fragments, Fragment
from typing import Optional, List


class Markdown(MathOutput):
    def __init__(self, file_name: Optional[str] = None):
        self._lines = []
        self._file_name = file_name

    def __call__(self, *args, **kwargs):
        fragments = entities_to_fragments(*args)

        if kwargs.get("inline", False):
            self._write_fragments_inline(fragments)
        else:
            self._write_fragments_block(fragments)

    def _write_fragments_inline(self, fragments: List[Fragment]):
        elements = []
        for f in fragments:
            if f.is_latex:
                elements.append(f"${f.text}$")
            else:
                elements.append(f.text)
        self._lines.append(" ".join(elements))

    def _write_fragments_block(self, fragments: List[Fragment]):
        # Each string will be a new line, but each latex fragment will be wrapped in $$ to make it a block
        for f in fragments:
            if f.is_latex:
                self._lines.append(f"$${f.text}$$\n")
            else:
                self._lines.append(f.text)

    def get_text(self):
        return "\n".join(self._lines)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._file_name:
            self.write()
        return False

    def write(self, file_name: Optional[str] = None):
        file_name = file_name or self._file_name
        if file_name is None:
            raise ValueError("No file name provided and none was set during initialization")
        with open(file_name, "w") as handle:
            handle.write(self.get_text())
