from dataclasses import dataclass

import imgui

from generator.ctrl.steps.Step import StepConfig
from util import canonize_number

_MIN_NODES = 10
_MAX_NODES = 500_000


@dataclass
class MeshConfig:
    n_nodes: int = 400


class MeshCreationStepConfig(StepConfig[MeshConfig]):
    def __init__(self):
        super().__init__("Mesh", MeshConfig())

    def _create_step(self, config: MeshConfig):
        from generator.ctrl.steps.mesh.step import MeshCreationStep
        return MeshCreationStep(config=config)

    def _render_config(self):
        _, self._edited_data.n_nodes = imgui.drag_int("nodes", self._edited_data.n_nodes, 10, _MIN_NODES, _MAX_NODES)
        area, suffix = canonize_number(self._edited_data.n_nodes)
        imgui.text_unformatted(f"nodes: {area}{suffix.upper()}")
