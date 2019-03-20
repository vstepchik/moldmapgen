from dataclasses import dataclass

from generator.ctrl.steps.Step import StepConfig, GeneratorStep


@dataclass
class TectonicsConfig:
    n_plates: int = 400


class TectonicsCreationStep(GeneratorStep[TectonicsConfig]):
    pass


class TectonicsCreationStepConfig(StepConfig[TectonicsConfig]):
    def __init__(self):
        super().__init__("Tectonics", TectonicsConfig())

    def _create_step(self, config: TectonicsConfig) -> TectonicsCreationStep:
        return TectonicsCreationStep(config=config)
