'''
Translated from source code from https://learnopengl.com/

6.4 Shaders
Draws triangle that fades in and out of being green to black
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
'''

from OpenGL import GL as gl
import glfw
import numpy as np
import sys

# settings
WIDTH, HEIGHT = 800, 600

vertexShaderSource = """
#version 330 core
layout (location = 0) in vec3 aPos;
void main()
{
   gl_Position = vec4(aPos, 1.0);
};
"""

fragmentShaderSource = """
#version 330 core
out vec4 color;
uniform vec4 ourColor;
void main()
{
    color = ourColor;
}
"""

class VBO:
    _buffer_type = gl.GL_ARRAY_BUFFER

    def __init__(self, data):
        self._vbo = gl.GLuint()
        gl.glGenBuffers(1, self._vbo)
        self.bind()
        gl.glBufferData(self._buffer_type, data, gl.GL_STATIC_DRAW)

    def __del__(self):
        gl.glDeleteBuffers(1, self._vbo)

    def bind(self):
        gl.glBindBuffer(self._buffer_type, self._vbo)

    def unbind(self):
        gl.glBindBuffer(self._buffer_type, 0)

class EBO(VBO):
    _buffer_type = gl.GL_ELEMENT_ARRAY_BUFFER

class VAO:
    def __init__(self):
        self._vao = gl.GLuint()
        gl.glGenVertexArrays(1, self._vao)
        self.bind()

    def __del__(self):
        gl.glDeleteVertexArrays(1, self._vao)

    def bind(self):
        gl.glBindVertexArray(self._vao)

    def unbind(self):
        gl.glBindVertexArray(0)

def shader(vs_src, frag_src):

    # build and compile shader program

    # vertex shader
    vertexShader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
    gl.glShaderSource(vertexShader, vs_src)
    gl.glCompileShader(vertexShader);
    if not gl.glGetShaderiv(vertexShader, gl.GL_COMPILE_STATUS):
        infoLog = gl.glGetShaderInfoLog(vertexShader).decode()
        raise Exception("ERROR::SHADER::VERTEX::COMPILATION_FAILED\n" + infoLog)

    # fragment shader
    fragmentShader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
    gl.glShaderSource(fragmentShader, frag_src)
    gl.glCompileShader(fragmentShader);
    if not gl.glGetShaderiv(fragmentShader, gl.GL_COMPILE_STATUS):
        infoLog = gl.glGetShaderInfoLog(fragmentShader).decode()
        raise Exception("ERROR::SHADER::FRAGMENT::COMPILATION_FAILED\n" + infoLog)

    # link shaders
    shaderProgram = gl.glCreateProgram()
    gl.glAttachShader(shaderProgram, vertexShader)
    gl.glAttachShader(shaderProgram, fragmentShader)
    gl.glLinkProgram(shaderProgram)
    if not gl.glGetProgramiv(shaderProgram, gl.GL_LINK_STATUS):
        infoLog = gl.glGetProgramInfoLog(shaderProgram).decode()
        raise Exception("ERROR::SHADER::PROGRAM::LINKING_FAILED\n" + infoLog)
    gl.glDeleteShader(vertexShader)
    gl.glDeleteShader(fragmentShader)

    return shaderProgram


def main():

    # declare draw method so it can be reused during resizing
    def draw():
        gl.glClearColor(0.2, 0.3, 0.3, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        gl.glUseProgram(shaderProgram)

        vao.bind()

        # update shader uniform
        timeValue = glfw.get_time()
        greenValue = np.sin(timeValue) / 2.0 + 0.5
        vertexColorLocation = gl.glGetUniformLocation(shaderProgram, "ourColor")
        gl.glUniform4f(vertexColorLocation, 0.0, greenValue, 0.0, 1.0)

        gl.glDrawElements(gl.GL_TRIANGLES, 3*indices.shape[0], gl.GL_UNSIGNED_INT, None)
    
        vao.unbind()

        glfw.swap_buffers(window)
        
    # declaring resize callback in main to allow access to variables
    def window_size_callback(window, width, height):
        gl.glViewport(0, 0, width, height)
        # calling draw to allow drawing while resizing
        draw()

    # glfw: initialize and configure
    
    glfw.init()

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE) # No deprecated functions
    glfw.window_hint(glfw.RESIZABLE, gl.GL_TRUE)

    # checking if run on Mac OS X
    if sys.platform == 'darwin':
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    # glfw window creation
    window = glfw.create_window(WIDTH, HEIGHT, 'LearnOpenGL', None, None)   # tutorial: (800, 600...
    if window is None:
        glfw.terminate()
        raise Exception("ERROR: Failed to create GLFW window")

    glfw.make_context_current(window)

    glfw.set_key_callback(window, key_callback)

    width, height = glfw.get_framebuffer_size(window)
    glfw.set_window_size_callback(window, window_size_callback)

    shaderProgram = shader(vertexShaderSource, fragmentShaderSource)

    # set up vertex data (and buffer(s)) and configure vertex attributes

    vertices = np.array(
            [[ 0.5, -0.5, 0.0],   # bottom right 
             [-0.5, -0.5, 0.0],   # bottom left
             [ 0.0, 0.5,  0.0]],  # top   
            dtype=np.float32)

    indices = np.array(
            [[0, 1, 2]],
            dtype=np.int32)

    vao = VAO()
    vbo = VBO(vertices)
    ebo = EBO(indices)

    stride = vertices.itemsize * vertices.shape[1]
    offset = gl.ctypes.c_void_p(vertices.itemsize * 0)

    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, stride, offset)
    gl.glEnableVertexAttribArray(0)     # location = 0

    vbo.unbind()
    vao.unbind()
    ebo.unbind()

    # to put in wireframe mode
    # gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)

    # render loop
    while not glfw.window_should_close(window):
        glfw.poll_events()

        draw()
    
    del vbo, ebo, vao
    glfw.terminate()

    return 0

def key_callback(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

if __name__ == "__main__":
    main()
