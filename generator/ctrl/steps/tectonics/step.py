from generator.ctrl.steps.step import GeneratorStep
from generator.ctrl.steps.tectonics.config import TectonicsConfig
from generator.world import World


class TectonicsCreationStep(GeneratorStep[TectonicsConfig]):
    def run(self, world: World):
        pass
