from concurrent.futures import Future
from concurrent.futures.thread import ThreadPoolExecutor
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
        self.__executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=1)
        self.__step_running: bool = False

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

        if not self.__step_running and imgui.button("Apply"):
            step = selected_step.create_step()
            self.__step_running = True
            self.__executor.submit(step.run, self.__world).add_done_callback(self.__handle_step_complete)
        if selected_step.dirty:
            imgui.same_line()
            if imgui.button("Reset"):
                selected_step.reset()

        imgui.columns()
        imgui.separator()

        selected_step.render()

        imgui.end()

    def __handle_step_complete(self, step_result_future: Future):
        res = step_result_future.result()
        self.__world[res.__class__] = res
        self.__step_running = False
