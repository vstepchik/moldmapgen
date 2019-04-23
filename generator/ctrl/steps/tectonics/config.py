from dataclasses import dataclass

import imgui

from generator.ctrl.steps.step import StepConfig


@dataclass
class TectonicsConfig:
    n_plates: int = 7


class TectonicsCreationStepConfig(StepConfig[TectonicsConfig]):
    def __init__(self):
        super().__init__("Tectonics", TectonicsConfig())

    def _create_step(self, config: TectonicsConfig):
        from generator.ctrl.steps.tectonics.step import TectonicsCreationStep
        return TectonicsCreationStep(config=config)

    def _render_config(self):
        _, self._edited_data.n_plates = imgui.drag_int("plates", self._edited_data.n_plates, 0.5, 1, 100)
