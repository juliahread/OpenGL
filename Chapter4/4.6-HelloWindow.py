"""
4.6 Hello Window
Initializes a window, has key event close, and sets background color
Some differences exist between solution code, pdf description, and this code
"""

from OpenGL import GL as gl
import glfw

WIDTH, HEIGHT = 800, 600

def main():
    
    print("Starting GLFW context, OpenGL 3.3")

    glfw.init()

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE) # No deprecated functions
    glfw.window_hint(glfw.RESIZABLE, gl.GL_FALSE)

    #FIXIT: test for Mac and add
    #       glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);

    window = glfw.create_window(WIDTH, HEIGHT, 'LearnOpenGL', None, None)

    if window is None:
        glfw.terminate()
        raise Exception("ERROR: Failed to create GLFW window")

    glfw.make_context_current(window)

    glfw.set_key_callback(window, key_callback)

    # illustration for if the window is resized
    width, height = glfw.get_framebuffer_size(window)

    gl.glViewport(0, 0, width, height)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        gl.glClearColor(0.2, 0.3, 0.3, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        glfw.swap_buffers(window)

    glfw.terminate()

    return 0

def key_callback(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

if __name__ == "__main__":
    main()
