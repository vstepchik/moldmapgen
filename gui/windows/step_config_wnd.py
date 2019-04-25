from typing import List

import imgui

from generator.ctrl.steps.step import StepConfig
from generator.world import World


class StepConfigWindow:
    def __init__(self, world: World, steps: List[StepConfig]) -> None:
        if not steps:
            raise ValueError("Steps should contain at least single item")
        self.expanded = True
        self.open = True

        self.__world = world

        self.steps: List[StepConfig] = steps
        self.selected_step_idx: int = 0

    def render(self):
        if not self.open:
            return

        self.expanded, self.open = imgui.begin("Configuration window", True)
        if not self.expanded:
            imgui.end()
            return

        imgui.columns(2)

        names = [f"{s.name}*" if s.dirty else s.name for s in self.steps]
        _, self.selected_step_idx = imgui.listbox("Step", self.selected_step_idx, names, min(5, len(self.steps)))
        selected_step = self.steps[self.selected_step_idx]

        imgui.next_column()

        if imgui.button("Apply"):
            step = selected_step.create_step()
            step.run(self.__world)
        if selected_step.dirty:
            imgui.same_line()
            if imgui.button("Reset"):
                selected_step.reset()

        imgui.columns()
        imgui.separator()

        selected_step.render()

        imgui.end()
