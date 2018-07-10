'''
Translated from source code from https://learnopengl.com/

6.8.3 Shaders
Set color to and output the vertex position to the fragment shader
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

class ShaderProgram:
    def __init__(self, vertex_source, fragment_source, geometry_source=None):

        try:
            with open(vertex_source) as fh:
                vertex_source = fh.read()
        except (FileNotFoundError, OSError) as e:
            pass

        try:
            with open(fragment_source) as fh:
                fragment_source = fh.read()
        except (FileNotFoundError, OSError) as e:
            pass

        try:
            if geometry_source:
                with open(geometry_source) as fh:
                    geometry_source = fh.read()
        except (FileNotFoundError, OSError) as e:
            pass

        vertexShader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        gl.glShaderSource(vertexShader, vertex_source)
        gl.glCompileShader(vertexShader)
        if not gl.glGetShaderiv(vertexShader, gl.GL_COMPILE_STATUS):
            infoLog = gl.glGetShaderInfoLog(vertexShader).decode()
            raise Exception("ERROR::SHADER::VERTEX::COMPILATION_FAILED\n" + infoLog)

        fragmentShader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        gl.glShaderSource(fragmentShader, fragment_source)
        gl.glCompileShader(fragmentShader)
        if not gl.glGetShaderiv(fragmentShader, gl.GL_COMPILE_STATUS):
            infoLog = gl.glGetShaderInfoLog(fragmentShader).decode()
            raise Exception("ERROR::SHADER::FRAGMENT::COMPILATION_FAILED\n" + infoLog)

        if geometry_source:
            geometryShader = gl.glCreateShader(gl.GL_GEOMETRY_SHADER)
            gl.glShaderSource(geometryShader, geometry_source)
            gl.glCompileShader(geometryShader)
            if not gl.glGetShaderiv(geometryShader, gl.GL_COMPILE_STATUS):
                infoLog = gl.glGetShaderInfoLog(geometryShader).decode()
                raise Exception("ERROR::SHADER::GEOMETRY::COMPILATION_FAILED\n" + infoLog)

        self.Program = gl.glCreateProgram()
        gl.glAttachShader(self.Program, vertexShader)
        gl.glAttachShader(self.Program, fragmentShader)
        if geometry_source:
            gl.glAttachShader(self.Program, geometryShader)
        gl.glLinkProgram(self.Program)
        if not gl.glGetProgramiv(self.Program, gl.GL_LINK_STATUS):
            infoLog = gl.glGetProgramInfoLog(self.Program).decode()
            raise Exception("ERROR::SHADER::PROGRAM::LINKING_FAILED\n" + infoLog)
        gl.glDeleteShader(vertexShader)
        gl.glDeleteShader(fragmentShader)
        if geometry_source:
            gl.glDeleteShader(geometryShader)

        self.use()

    def use(self):
        gl.glUseProgram(self.Program)

# settings
WIDTH, HEIGHT = 800, 600

vertexShaderSource = """
#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;
out vec3 ourColor;
void main()
{
   gl_Position = vec4(aPos, 1.0);
   ourColor = aPos;
};
"""

fragmentShaderSource = """
#version 330 core
out vec4 color;
in vec3 ourColor;
void main()
{
    color = vec4(ourColor, 1.0);
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

def main():

    # declare draw method so it can be reused during resizing
    def draw():
        gl.glClearColor(0.2, 0.3, 0.3, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        shaderProgram.use()

        vao.bind()

        # update shader uniform
        timeValue = glfw.get_time()
        greenValue = np.sin(timeValue) / 2.0 + 0.5
        vertexColorLocation = gl.glGetUniformLocation(shaderProgram.Program, "ourColor")
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

    shaderProgram = ShaderProgram(vertexShaderSource, fragmentShaderSource)

    # set up vertex data (and buffer(s)) and configure vertex attributes

    vertices = np.array(
            [[ 0.5, -0.5, 0.0, 1.0, 0.0, 0.0],  # bottom right
             [-0.5, -0.5, 0.0, 0.0, 1.0, 0.0],  # bottom left
             [ 0.0,  0.5, 0.0, 0.0, 0.0, 1.0]], # top   
            dtype=np.float32)

    indices = np.array(
            [[0, 1, 2]],
            dtype=np.int32)

    vao = VAO()
    vbo = VBO(vertices)
    ebo = EBO(indices)

    stride = vertices.itemsize * vertices.shape[1]
    offset0 = gl.ctypes.c_void_p(vertices.itemsize * 0)
    offset1 = gl.ctypes.c_void_p(vertices.itemsize * 3)

    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, stride, offset0)
    gl.glEnableVertexAttribArray(0)     # location = 0

    gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, stride, offset1)
    gl.glEnableVertexAttribArray(1)     # location = 1

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

