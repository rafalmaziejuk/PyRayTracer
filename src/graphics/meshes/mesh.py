from graphics.vertex_array import VertexArray
from graphics.vertex_buffer import ElementBuffer, VertexBuffer, BufferLayout, Types
from graphics.texture import Texture

class Mesh():
    def __init__(self, position, vertices, indices, layout):
        self.position = position
        self.modelMatrix = None
        self.color = None
        self.texture = None

        vertexBuffer = VertexBuffer(vertices)
        vertexBuffer.layout = BufferLayout(layout)

        elementBuffer = ElementBuffer(indices)
        
        self.vertexArray = VertexArray()
        self.vertexArray.set_vertex_buffer(vertexBuffer)
        self.vertexArray.set_element_buffer(elementBuffer)

    def cleanup(self):
        self.vertexArray.cleanup()
        if self.texture:
            self.texture.cleanup()

    def set_texture(self, filename):
        self.texture = Texture(filename)

    def set_color(self, color):
        self.color = color

    def bind(self, slot=0):
        self.vertexArray.bind()
        if self.texture:
            self.texture.bind(slot)

    def unbind(self):
        self.vertexArray.unbind()
        if self.texture:
            self.texture.unbind()
