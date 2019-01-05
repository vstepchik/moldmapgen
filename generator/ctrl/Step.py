import imgui


class Step:
    def __init__(self, name: str) -> None:
        self._dirty: bool = True
        self.name: str = name


class ConfigurableStep(Step):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def render_config(self) -> None:
        label = f"{self.name} configuration"
        if self._dirty:
            label += '*'

        imgui.text(label)
        imgui.text("/// NOT IMPLEMENTED ///")
