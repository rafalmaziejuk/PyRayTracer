from graphics.vertex_buffer import VertexBuffer, BufferLayout, Types
from graphics.vertex_array import VertexArray
from OpenGL.GL import (
    GL_FALSE,
    GL_WRITE_ONLY, GL_TEXTURE_2D, GL_UNSIGNED_BYTE, GL_RGBA8,
    glBindTexture, glBindImageTexture, glTexImage2D
)

VERTICES = [
         #position     #texCoords
    -1.0, -1.0,  0.0,   0.0, 0.0,
     1.0, -1.0,  0.0,   1.0, 0.0,
    -1.0,  1.0,  0.0,   0.0, 1.0,
     1.0,  1.0,  0.0,   1.0, 1.0,
    ]

class FullscreenQuad():
    def __init__(self, renderTexture):
        self.renderTexture = renderTexture

        vertexBuffer = VertexBuffer(VERTICES)
        vertexBuffer.layout = BufferLayout([Types.FLOAT3, Types.FLOAT2])

        self.vertexArray = VertexArray()
        self.vertexArray.set_vertex_buffer(vertexBuffer)

    def cleanup(self):
        self.renderTexture.cleanup()
        self.vertexArray.cleanup()

    def bind(self):
        self.renderTexture.bind(0)
        self.vertexArray.bind()

    def unbind(self):
        self.vertexArray.unbind()

    def resize(self, width, height):
        texture = self.renderTexture
        texture.width = width
        texture.height = height

        glBindTexture(GL_TEXTURE_2D, texture.id)
        glTexImage2D(GL_TEXTURE_2D, 0, texture.internalFormat, texture.width, texture.height, 0, texture.dataFormat, GL_UNSIGNED_BYTE, None)
        glBindImageTexture(0, texture.id, 0, GL_FALSE, 0, GL_WRITE_ONLY, GL_RGBA8)
