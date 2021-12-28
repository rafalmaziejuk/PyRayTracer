from vertex_array import VertexArray
from vertex_buffer import VertexBuffer, ElementBuffer, BufferLayout, Types
from shader import Shader
from OpenGL.GL import *
from glm import value_ptr, ortho, translate, scale, mat4, vec3

class RendererData():
    def __init__(self, width, height):
        self.projectionMatrix = ortho(0.0, width, height, 0.0, -1.0, 1.0)
        self.shader = Shader('shaders/shader.vert', 'shaders/shader.frag')

        self.shader.bind()
        self.shader.set_mat4('projection', value_ptr(self.projectionMatrix))
		
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
        self.shader.cleanup()
        self.vertexArray.cleanup()

rendererData = None

class Renderer():
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
    def draw(position, size, color):
        model = translate(mat4(1.0), vec3(position, 0.0)) * scale(mat4(1.0), vec3(size, 1.0))

        rendererData.shader.bind()
        rendererData.shader.set_vec3f('color', vec3(color))
        rendererData.shader.set_mat4('model', value_ptr(model))

        rendererData.vertexArray.bind()
        glDrawElements(GL_TRIANGLES, rendererData.vertexArray.elementBuffer.elementCount, GL_UNSIGNED_INT, None)
