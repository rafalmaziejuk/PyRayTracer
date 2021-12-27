from window import Window
from renderer import Renderer
from vertex_array import VertexArray
from vertex_buffer import VertexBuffer, ElementBuffer, BufferLayout, Types
from OpenGL.GL import *

vertexShaderSource = """
    #version 330 core
    layout (location = 0) in vec3 aPos;
    void main()
    {
       gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
    }
    """

fragmentShaderSource = """
    #version 330 core
    out vec4 FragColor;
    void main()
    {
        FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
    }
    """

class Application():
    def __init__(self, width=800, height=600, name="PyRayTracer"):
        self.window = Window(width, height, name)

    def run(self):
        vertexShader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertexShader, vertexShaderSource)
        glCompileShader(vertexShader)

        fragmentShader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragmentShader, fragmentShaderSource)
        glCompileShader(fragmentShader)

        shaderProgram = glCreateProgram()
        glAttachShader(shaderProgram, vertexShader)
        glAttachShader(shaderProgram, fragmentShader)
        glLinkProgram(shaderProgram)
        
        glDeleteShader(vertexShader);
        glDeleteShader(fragmentShader);
        glUseProgram(shaderProgram)
        
        vertices = [
             0.5,  0.5, 0.0,
             0.5, -0.5, 0.0,
            -0.5, -0.5, 0.0,
            -0.5,  0.5, 0.0 
        ]
        indices = [
            0, 1, 3,
            1, 2, 3
        ]

        vertexBuffer = VertexBuffer(vertices)
        vertexBuffer.layout = BufferLayout([Types.FLOAT3])

        elementBuffer = ElementBuffer(indices)
        
        vertexArray = VertexArray()
        vertexArray.set_vertex_buffer(vertexBuffer)
        vertexArray.set_element_buffer(elementBuffer)

        while self.window.is_running():
            self.window.process_input()

            Renderer.clear()

            glUseProgram(shaderProgram);
            glDrawElements(GL_TRIANGLES, vertexArray.elementBuffer.elementCount, GL_UNSIGNED_INT, None)

            self.window.update()

        vertexArray.cleanup()
        self.window.cleanup()
