from window import Window
from renderer import Renderer
from vertex_array import VertexArray
from vertex_buffer import VertexBuffer, ElementBuffer, BufferLayout, Types
from shader import Shader
from OpenGL.GL import *

class Application():
    def __init__(self, width=800, height=600, name='PyRayTracer'):
        self.window = Window(width, height, name)

    def run(self):
        shader = Shader('shaders/shader.vert', 'shaders/shader.frag')
        shader.bind()

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

            glDrawElements(GL_TRIANGLES, vertexArray.elementBuffer.elementCount, GL_UNSIGNED_INT, None)

            self.window.update()

        shader.cleanup()
        vertexArray.cleanup()
        self.window.cleanup()
