from generator.ctrl.steps.space.config import SpaceConfig
from generator.ctrl.steps.step import GeneratorStep
from generator.world import World, Space


class SpaceCreationStep(GeneratorStep[SpaceConfig]):
    def run(self, world: World):
        world[Space] = Space(self.config.width, self.config.height)
