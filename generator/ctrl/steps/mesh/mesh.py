from dataclasses import dataclass

from generator.ctrl.steps.Step import StepConfig, GeneratorStep


@dataclass
class MeshConfig:
    n_vertices: int = 400


class MeshCreationStep(GeneratorStep[MeshConfig]):
    pass


class MeshCreationStepConfig(StepConfig[MeshConfig]):
    def __init__(self):
        super().__init__("Mesh", MeshConfig())

    def _create_step(self, config: MeshConfig) -> MeshCreationStep:
        return MeshCreationStep(config=config)
