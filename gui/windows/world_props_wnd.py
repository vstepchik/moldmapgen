import imgui

from generator.world import World, WorldProp, Space, Mesh, Tectonics


class WorldPropertiesWindow:
    def __init__(self, world: World) -> None:
        self.expanded = True
        self.open = True

        self.__world: World = world

    def render(self):
        if not self.open:
            return

        self.expanded, self.open = imgui.begin("World props", True)
        if not self.expanded:
            imgui.end()
            return

        self.render_props()

        imgui.end()

    def render_props(self):
        for prop_cls, val in self.__world.props.items():
            if imgui.tree_node(prop_cls.__name__):
                self.__render_prop(val)
                imgui.tree_pop()

    def __render_prop(self, p: WorldProp):
        if isinstance(p, Space):
            imgui.text_unformatted(f"size: {p.width}x{p.height}")
            imgui.text_unformatted(f"area: {p.width * p.height}")
        elif isinstance(p, Mesh):
            imgui.text_unformatted(f"num points: {len(p.points)}")
        elif isinstance(p, Tectonics):
            imgui.text_unformatted(f"num plates: {len(p.plates)}")
            if imgui.tree_node("plates"):
                cols = ["N", "size", "color", "velocity", "spin"]
                imgui.columns(len(cols))
                for col in cols:
                    imgui.text_unformatted(col)
                    imgui.next_column()
                imgui.separator()
                for i, pl in enumerate(p.plates):
                    imgui.text_unformatted(str(i))
                    imgui.next_column()
                    imgui.text_unformatted(f"{len(pl.mesh_points)}")
                    imgui.next_column()
                    imgui.color_button(f"##plate_color_{i}", *pl.color_rgb)
                    imgui.next_column()
                    imgui.text_unformatted(f"{pl.velocity}")
                    imgui.next_column()
                    imgui.text_unformatted(f"{pl.spin_rad}")
                    imgui.next_column()
                imgui.columns()
                imgui.tree_pop()
        else:
            imgui.text_unformatted("NO REPR")
