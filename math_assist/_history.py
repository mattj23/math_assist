from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional, List, Callable
from copy import copy
from ._common import MathOutput


class IndexSource:
    def __init__(self, start_at: int = 0):
        self._index = start_at

    def take(self) -> int:
        index = self._index
        self._index += 1
        return index


class HistoryTarget(ABC):
    @abstractmethod
    def get_last_state(self) -> Any:
        pass

    @abstractmethod
    def get_current_state(self) -> Any:
        pass


@dataclass
class WorkStep:
    index: int
    description: str
    args: List[Any]
    before: Any
    after: Any
    suffix: Optional[str] = None
    children: Optional[List[WorkStep]] = None


def _write_step(step: WorkStep, output: MathOutput):
    output(step.description, *step.args, step.suffix or "", inline=True)
    output(step.after)


@dataclass
class ParentHistory:
    tag: str
    history: WorkingHistory


class ParentStepContext:
    def __init__(self, history: WorkingHistory, tag: str):
        self._history = history
        self.tag = tag
        self.sub_steps = []

    def append_step(self, step: WorkStep):
        self.sub_steps.append(step)

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._history.end_combined_step()


class WorkingHistory:
    def __init__(self, index_source: Optional[IndexSource] = None,
                 parent: Optional[ParentHistory] = None,
                 current_state: Any = None,
                 get_combined_state: Optional[Callable[[], Any]] = None):
        self._index_source = index_source or IndexSource()

        self._last_state = None
        self._current_state = current_state

        self._parent = parent
        if self._parent is not None:
            self._index_source = self._parent.history.index_source

        self._history = []
        self._outputs: List[MathOutput] = []

        self._get_combined_state = get_combined_state

        self._combined_context: Optional[ParentStepContext] = None

    @property
    def index_source(self):
        return self._index_source

    def combined_step(self, tag: str):
        self._combined_context = ParentStepContext(self, tag)
        return self._combined_context

    def end_combined_step(self):
        if self._combined_context:
            first_step = self._combined_context.sub_steps[0]
            last_step = self._combined_context.sub_steps[-1]

            step = WorkStep(self._index_source.take(),
                            first_step.description,
                            first_step.args,
                            first_step.before,
                            last_step.after,
                            suffix=self._combined_context.tag,
                            children=self._combined_context.sub_steps)
            self._append_step(step)
        self._combined_context = None

    def as_parent(self, tag: str):
        return ParentHistory(tag, self)

    def update(self, new_state: Any):
        self._last_state = self._current_state
        self._current_state = new_state

    def append(self, description: str, arg_list: List, new_state: Any):
        self.update(new_state)
        step = WorkStep(self._index_source.take(), description, arg_list, self._last_state, self._current_state)
        self._append_step(step)

    def _append_step(self, step: WorkStep):
        self._history.append(step)

        if self._parent:
            self._parent.history._append_by_child(step, self._parent.tag)

        for output in self._outputs:
            _write_step(step, output)

    def _append_by_child(self, step: WorkStep, tag: str):
        self.update(self._get_combined_state())

        step = copy(step)
        step.suffix = f" on {tag}"
        step.before = self._last_state
        step.after = self._current_state
        if self._combined_context:
            self._combined_context.append_step(step)
        else:
            self._append_step(step)

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
