from generator.ctrl.Step import ConfigurableStep


class MeshCreationStep(ConfigurableStep):
    def __init__(self):
        super().__init__("Mesh")
