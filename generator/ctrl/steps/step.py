import abc
from copy import deepcopy
from typing import TypeVar, Generic

from generator.world import World

_CT = TypeVar("_CT")


class GeneratorStep(Generic[_CT]):
    def __init__(self, config: _CT) -> None:
        self.config: _CT = config

    @abc.abstractmethod
    def run(self, world: World):
        pass


class StepConfig(Generic[_CT]):
    def __init__(self, name: str, initial_data: _CT) -> None:
        self._data: _CT = deepcopy(initial_data)
        self._edited_data: _CT = initial_data
        self.name: str = name

    @property
    def dirty(self) -> bool:
        return self._data != self._edited_data

    def reset(self):
        self._edited_data = deepcopy(self._data)

    def create_step(self) -> GeneratorStep[_CT]:
        self._data = deepcopy(self._edited_data)
        return self._create_step(self._data)

    @abc.abstractmethod
    def _create_step(self, config: _CT) -> GeneratorStep[_CT]:
        pass

    def render(self):
        self._render_config()

    @abc.abstractmethod
    def _render_config(self):
        pass
