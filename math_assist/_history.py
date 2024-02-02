from dataclasses import dataclass
from typing import Any, Optional, List
from ._common import MathOutput


class IndexSource:
    def __init__(self, start_at: int = 0):
        self._index = start_at

    def take(self) -> int:
        index = self._index
        self._index += 1
        return index


@dataclass
class WorkStep:
    index: int
    description: str
    args: List[Any]
    before: Any
    after: Any


def _write_step(step: WorkStep, output: MathOutput):
    output(step.description, *step.args, inline=True)
    output(step.after)


class WorkingHistory:
    def __init__(self, index_source: Optional[IndexSource] = None):
        self._index_source = index_source if index_source else IndexSource()
        self._history = []
        self._outputs: List[MathOutput] = []

    def append(self, description: str, arg_list: List, before: Optional[Any] = None, after: Optional[Any] = None):
        step = WorkStep(self._index_source.take(), description, arg_list, before, after)
        self._history.append(step)
        for output in self._outputs:
            _write_step(step, output)

    def __iter__(self):
        return iter(self._history)

    def __getitem__(self, item):
        return self._history[item]

    def _write_start_state(self, output: MathOutput):
        output("Initial state")
        output(self._history[0].before)

    def write_all_to(self, output: MathOutput, skip_start_state: bool = False):
        if not skip_start_state:
            self._write_start_state(output)

        for step in self._history:
            _write_step(step, output)

    def attach_output(self, output: MathOutput):
        if output not in self._outputs:
            self._outputs.append(output)

    def detach_output(self, output: MathOutput):
        if output in self._outputs:
            self._outputs.remove(output)

    def detach_all_outputs(self):
        self._outputs = []