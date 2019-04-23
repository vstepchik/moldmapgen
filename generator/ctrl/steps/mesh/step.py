from generator.ctrl.steps.mesh.config import MeshConfig
from generator.ctrl.steps.step import GeneratorStep
from generator.world import World


class MeshCreationStep(GeneratorStep[MeshConfig]):
    def run(self, world: World):
        pass
