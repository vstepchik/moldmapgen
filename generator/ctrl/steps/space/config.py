from dataclasses import dataclass
from math import sqrt

import imgui

from generator.ctrl.steps.step import StepConfig
from util import canonize_number

_MIN_SIZE = 100
_MAX_SIZE = 50_000


@dataclass
class SpaceConfig:
    width: int = 2000
    height: int = 2000

    @property
    def area(self) -> int:
        return self.width * self.height

    @property
    def perimeter(self) -> int:
        return (self.width + self.height) * 2

    @property
    def diagonal(self) -> float:
        return sqrt(self.width * self.width + self.height * self.height)

    @property
    def ratio(self) -> float:
        return self.width / self.height


class SpaceCreationStepConfig(StepConfig[SpaceConfig]):
    def __init__(self):
        super().__init__("Space", SpaceConfig())
        self.__square_world: bool = True

    def _create_step(self, config: SpaceConfig):
        from generator.ctrl.steps.space.step import SpaceCreationStep
        return SpaceCreationStep(config)

    def _render_config(self):
        _, self.__square_world = imgui.checkbox("Square world", self.__square_world)
        if self.__square_world:
            _, size = imgui.drag_int("size", self._edited_data.width, 10, _MIN_SIZE, _MAX_SIZE)
            self._edited_data.width = size
            self._edited_data.height = size
        else:
            _, self._edited_data.width = imgui.drag_int("width", self._edited_data.width, 10, _MIN_SIZE, _MAX_SIZE)
            _, self._edited_data.height = imgui.drag_int("height", self._edited_data.height, 10, _MIN_SIZE, _MAX_SIZE)

        area, suffix = canonize_number(self._edited_data.area)
        imgui.text_unformatted(f"area: {area}{suffix.upper()}")
