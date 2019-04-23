import numpy as np

from generator.ctrl.steps.mesh.config import MeshConfig
from generator.ctrl.steps.step import GeneratorStep
from generator.world import World, Mesh


class MeshCreationStep(GeneratorStep[MeshConfig]):
    def run(self, world: World):
        world[Mesh] = Mesh(np.asarray([[1., 1.], [1., 0.]]))
