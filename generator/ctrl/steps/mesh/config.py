from dataclasses import dataclass

from generator.ctrl.steps.Step import StepConfig


@dataclass
class MeshConfig:
    n_vertices: int = 400


class MeshCreationStepConfig(StepConfig[MeshConfig]):
    def __init__(self):
        super().__init__("Mesh", MeshConfig())

    def _create_step(self, config: MeshConfig):
        from generator.ctrl.steps.mesh.step import MeshCreationStep
        return MeshCreationStep(config=config)
