from generator.ctrl.steps.step import GeneratorStep
from generator.ctrl.steps.tectonics.config import TectonicsConfig
from generator.world import World, Tectonics, Plate


class TectonicsCreationStep(GeneratorStep[TectonicsConfig]):
    def run(self, world: World):
        world[Tectonics] = Tectonics([Plate(), Plate(spin_rad=0.57, color_rgb=(0.5, 0., 0.))])
