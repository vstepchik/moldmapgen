from generator.ctrl.steps.space.config import SpaceConfig
from generator.ctrl.steps.step import GeneratorStep
from generator.world import World


class SpaceCreationStep(GeneratorStep[SpaceConfig]):
    def run(self, world: World):
        pass
