from graphics.vertex_array import VertexArray
from graphics.vertex_buffer import VertexBuffer, ElementBuffer, BufferLayout, Types
from graphics.shader import Shader
from OpenGL.GL import *
from glm import value_ptr, ortho, translate, rotate, radians, scale, mat4, vec3

class RendererData():
    def __init__(self, width, height):
        self.projectionMatrix = ortho(0.0, width, height, 0.0, -1.0, 1.0)

        self.shaderSolid = Shader('shaders/shaderSolid2D.vert', 'shaders/shaderSolid2D.frag')
        self.shaderSolid.bind()
        self.shaderSolid.set_mat4('projection', value_ptr(self.projectionMatrix))

        self.shaderTexture = Shader('shaders/shaderTexture2D.vert', 'shaders/shaderTexture2D.frag')
        self.shaderTexture.bind()
        self.shaderTexture.set_mat4('projection', value_ptr(self.projectionMatrix))
        self.shaderTexture.set_int('texture0', 0)
		
        vertices = [
            -0.5, -0.5, 0.0, 0.0,
			 0.5, -0.5, 1.0, 0.0,
			 0.5,  0.5, 1.0, 1.0,
			-0.5,  0.5, 0.0, 1.0
        ]
        vertexBuffer = VertexBuffer(vertices)
        vertexBuffer.layout = BufferLayout([Types.FLOAT4])
        
        indices = [
            0, 1, 2,
            2, 3, 0
        ]
        elementBuffer = ElementBuffer(indices)
        
        self.vertexArray = VertexArray()
        self.vertexArray.set_vertex_buffer(vertexBuffer)
        self.vertexArray.set_element_buffer(elementBuffer)

    def cleanup(self):
        self.shaderSolid.cleanup()
        self.shaderTexture.cleanup()
        self.vertexArray.cleanup()

rendererData = None

class Renderer2D():
    @staticmethod
    def init(width, height, clearColor):
        glClearColor(clearColor[0], clearColor[1], clearColor[2], clearColor[3])
        glViewport(0, 0, width, height)

        global rendererData 
        rendererData = RendererData(width, height)
    
    @staticmethod
    def cleanup():
        rendererData.cleanup()
        
    @staticmethod
    def clear():
        glClear(GL_COLOR_BUFFER_BIT)

    @staticmethod
    def drawSolid(position, size, color, rotation=0.0):
        model = translate(mat4(1.0), vec3(position, 0.0)) * \
		        rotate(mat4(1.0), radians(rotation), vec3(0.0, 0.0, 1.0)) * \
		        scale(mat4(1.0), vec3(size, 1.0))

        rendererData.shaderSolid.bind()
        rendererData.shaderSolid.set_vec3f('color', vec3(color))
        rendererData.shaderSolid.set_mat4('model', value_ptr(model))

        rendererData.vertexArray.bind()
        glDrawElements(GL_TRIANGLES, rendererData.vertexArray.elementBuffer.elementCount, GL_UNSIGNED_INT, None)

    @staticmethod
    def drawTexture(position, texture, rotation=0.0):
        model = translate(mat4(1.0), vec3(position, 0.0)) * \
		        rotate(mat4(1.0), radians(rotation), vec3(0.0, 0.0, 1.0)) * \
		        scale(mat4(1.0), vec3(texture.size, 1.0))
        
        rendererData.shaderTexture.bind()
        rendererData.shaderTexture.set_mat4('model', value_ptr(model))
        
        texture.bind(GL_TEXTURE0)
        
        rendererData.vertexArray.bind()
        glDrawElements(GL_TRIANGLES, rendererData.vertexArray.elementBuffer.elementCount, GL_UNSIGNED_INT, None)
        texture.unbind()
