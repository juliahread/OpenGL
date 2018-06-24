"""
Translated from source code from https://learnopengl.com/

4.4 Hello Window
Initializes a window and has key event close and resize
Some differences exist between solution code, pdf description, and this code

Original work Copyright (c) 2015 Joey de Vries
Modified work Copyright (c) 2018 Julia Read

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
"""

from OpenGL import GL as gl
import glfw
import sys

# settings
WIDTH, HEIGHT = 800, 600

def main():
    
    # glfw: intialize and configure

    glfw.init()

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE) # No deprecated functions
    glfw.window_hint(glfw.RESIZABLE, gl.GL_TRUE)
    
    # checking if run on Mac OS X
    if sys.platform == 'darwin':
        glfwWindowHint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE);

    # glfw window creation
    window = glfw.create_window(WIDTH, HEIGHT, 'LearnOpenGL', None, None)

    if window is None:
        glfw.terminate()
        raise Exception("ERROR: Failed to create GLFW window")

    glfw.make_context_current(window)

    glfw.set_key_callback(window, key_callback)

    width, height = glfw.get_framebuffer_size(window)
    glfw.set_window_size_callback(window, window_size_callback)

    # render loop
    while not glfw.window_should_close(window):

        glfw.poll_events()
        glfw.swap_buffers(window)

    # glfw: terminate, clearing all previously allocated GLFW resources
    glfw.terminate()

    return 0

# process all input: query GLFW whether relevant keys are pressed/released this frame and react accordingly
def key_callback(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

#  glfw: whenever the window size changed (by OS or user resize) this callback function executes
def window_size_callback(window, width, height):
    gl.glViewport(0, 0, width, height)

if __name__ == "__main__":
    main()
