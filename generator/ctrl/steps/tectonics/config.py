from dataclasses import dataclass

from generator.ctrl.steps.Step import StepConfig


@dataclass
class TectonicsConfig:
    n_plates: int = 400


class TectonicsCreationStepConfig(StepConfig[TectonicsConfig]):
    def __init__(self):
        super().__init__("Tectonics", TectonicsConfig())

    def _create_step(self, config: TectonicsConfig):
        from generator.ctrl.steps.tectonics.step import TectonicsCreationStep
        return TectonicsCreationStep(config=config)