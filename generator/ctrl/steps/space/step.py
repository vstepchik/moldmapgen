from typing import Optional

from generator.ctrl.steps.space.config import SpaceConfig
from generator.ctrl.steps.step import GeneratorStep
from generator.world import World, Space


class SpaceCreationStep(GeneratorStep[SpaceConfig]):
    def run(self, world: World) -> Optional[Space]:
        return Space(self.config.width, self.config.height)
