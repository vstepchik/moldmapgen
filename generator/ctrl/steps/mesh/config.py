from dataclasses import dataclass

import imgui

from generator.ctrl.steps.Step import StepConfig


@dataclass
class MeshConfig:
    node_density: float = 0.017


class MeshCreationStepConfig(StepConfig[MeshConfig]):
    def __init__(self):
        super().__init__("Mesh", MeshConfig())

    def _create_step(self, config: MeshConfig):
        from generator.ctrl.steps.mesh.step import MeshCreationStep
        return MeshCreationStep(config=config)

    def _render_config(self):
        _, self._edited_data.node_density = imgui.drag_float(
            "node density", self._edited_data.node_density, 0.001, 0.0, 1.0,
        )
