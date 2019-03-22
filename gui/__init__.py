import sys
from threading import Thread

import OpenGL.GL as gl
import glfw
import imgui
from imgui.integrations.glfw import GlfwRenderer

from generator.ctrl.steps.mesh.config import MeshCreationStepConfig
from generator.ctrl.steps.space.config import SpaceCreationStepConfig
from generator.ctrl.steps.tectonics.config import TectonicsCreationStepConfig
from gui.fonts import init_fonts, get_font, FNT_3270_MED_28
from gui.windows.step_config_wnd import StepConfigWindow


class MoldMapGen(Thread):
    def __init__(self):
        super().__init__(daemon=False, name="Main Debug Window")
        self.__window = None

        self.__show_demo: bool = False
        self.__show_style_editor: bool = False
        self.__show_metrics: bool = False

        self.__step_config_window: StepConfigWindow = StepConfigWindow([
            SpaceCreationStepConfig(),
            MeshCreationStepConfig(),
            TectonicsCreationStepConfig(),
        ])

    def run(self):
        self.__window = self.__glfw_init_window("Mold Map Generator")
        imgui.create_context()
        init_fonts()
        window_renderer = GlfwRenderer(self.__window)

        while not glfw.window_should_close(self.__window):
            glfw.poll_events()
            window_renderer.process_inputs()

            imgui.new_frame()
            imgui.push_font(get_font(FNT_3270_MED_28))

            self.__main_menu_bar()
            self.__draw_windows()

            if self.__show_demo:
                imgui.show_test_window()
            if self.__show_style_editor:
                imgui.show_style_editor()
            if self.__show_metrics:
                imgui.show_metrics_window()

            gl.glClearColor(0.08, 0.08, 0.09, 1)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            imgui.pop_font()
            imgui.render()
            window_renderer.render(imgui.get_draw_data())
            glfw.swap_buffers(self.__window)

        window_renderer.shutdown()
        glfw.terminate()

    def __main_menu_bar(self):
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):
                clicked_quit, _selected_quit = imgui.menu_item("Quit")

                if clicked_quit:
                    glfw.set_window_should_close(self.__window, True)

                imgui.end_menu()

            if imgui.begin_menu("View", True):
                clicked, state = imgui.menu_item("Step config", None, self.__step_config_window.open)
                if clicked:
                    self.__step_config_window.open = state

                imgui.end_menu()

            if imgui.begin_menu("Imgui", True):
                clicked_demo, _ = imgui.menu_item("imgui demo", None, self.__show_demo)
                clicked_style_editor, _ = imgui.menu_item("style editor", None, self.__show_style_editor)
                clicked_metrics, _ = imgui.menu_item("imgui metrics", None, self.__show_style_editor)

                if clicked_demo:
                    self.__show_demo = not self.__show_demo

                if clicked_style_editor:
                    self.__show_style_editor = not self.__show_style_editor

                if clicked_metrics:
                    self.__show_metrics = not self.__show_metrics

                imgui.end_menu()

            imgui.end_main_menu_bar()

    def __draw_windows(self):
        if self.__show_demo:
            imgui.show_test_window()
        if self.__show_style_editor:
            imgui.show_style_editor()
        if self.__show_metrics:
            imgui.show_metrics_window()

        self.__step_config_window.render()

    @staticmethod
    def __glfw_init_window(window_name: str):
        width, height = 1920, 1080

        if not glfw.init():
            print("Could not initialize OpenGL context")
            sys.exit(1)

        monitor = glfw.get_primary_monitor()
        video_mode = glfw.get_video_mode(monitor)
        monitor_width_mm, monitor_height_mm = glfw.get_monitor_physical_size(monitor)
        mm_per_inch = 25.4
        dpi = video_mode.size.width / (monitor_width_mm / mm_per_inch)
        print(f"video_mode: {video_mode}, dpi: {dpi}")

        # OS X supports only forward-compatible core profiles from 3.2
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)
        glfw.window_hint(glfw.MAXIMIZED, gl.GL_TRUE)

        # Create a windowed mode window and its OpenGL context
        window = glfw.create_window(int(width), int(height), window_name, None, None)
        glfw.make_context_current(window)

        if not window:
            glfw.terminate()
            print("Could not initialize Window")
            sys.exit(2)

        return window
