from abc import ABC, abstractmethod


class MathOutput(ABC):
    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_text(self):
        pass
