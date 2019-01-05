import sys

import OpenGL.GL as gl
import glfw
import imgui
from imgui.integrations.glfw import GlfwRenderer

from generator.ctrl.steps.mesh import MeshCreationStep
from generator.ctrl.steps.space import SpaceCreationStep
from generator.ctrl.steps.tectonics import TectonicsCreationStep


def main():
    window = impl_glfw_init()
    impl = GlfwRenderer(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()

        imgui.new_frame()

        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):

                clicked_capture, selected_capture = imgui.menu_item("Capture view")
                clicked_quit, selected_quit = imgui.menu_item("Quit")

                if clicked_quit:
                    glfw.set_window_should_close(window, True)

                if selected_capture:
                    print("cs")

                imgui.end_menu()
            imgui.end_main_menu_bar()

        imgui.show_test_window()

        imgui.begin("Custom window", True)
        imgui.begin_group()
        imgui.text("Steps:")
        SpaceCreationStep().render_config()
        MeshCreationStep().render_config()
        TectonicsCreationStep().render_config()
        imgui.end_group()
        imgui.text_colored("Eggs", 0.2, 1., 0.)
        imgui.end()

        gl.glClearColor(0.05, 0.05, 0.05, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

    impl.shutdown()
    glfw.terminate()


def impl_glfw_init():
    width, height = 1280, 720
    window_name = "mold-map-gen"

    if not glfw.init():
        print("Could not initialize OpenGL context")
        sys.exit(1)

    # OS X supports only forward-compatible core profiles from 3.2
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(int(width), int(height), window_name, None, None)
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        sys.exit(2)

    return window


if __name__ == "__main__":
    main()
