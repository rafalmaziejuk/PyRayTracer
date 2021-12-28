from vertex_array import VertexArray
from vertex_buffer import VertexBuffer, ElementBuffer, BufferLayout, Types
from shader import Shader
from OpenGL.GL import *
from glm import value_ptr, perspective, translate, rotate, radians, scale, mat4, vec3

class RendererData():
    def __init__(self, width, height):
        self.projectionMatrix = perspective(radians(45.0), width / height, 0.1, 100.0)
        self.viewMatrix = translate(mat4(1.0), vec3(0.0, 0.0, -3.0))

        self.shaderTexture = Shader('shaders/shaderTexture3D.vert', 'shaders/shaderTexture3D.frag')
        self.shaderTexture.bind()
        self.shaderTexture.set_mat4('projection', value_ptr(self.projectionMatrix))
        self.shaderTexture.set_mat4('view', value_ptr(self.viewMatrix))
        self.shaderTexture.set_int('texture0', 0)
		
        vertices = [
            -0.5, -0.5, -0.5,  0.0, 0.0,
             0.5, -0.5, -0.5,  1.0, 0.0,
             0.5,  0.5, -0.5,  1.0, 1.0,
             0.5,  0.5, -0.5,  1.0, 1.0,
            -0.5,  0.5, -0.5,  0.0, 1.0,
            -0.5, -0.5, -0.5,  0.0, 0.0,

            -0.5, -0.5,  0.5,  0.0, 0.0,
             0.5, -0.5,  0.5,  1.0, 0.0,
             0.5,  0.5,  0.5,  1.0, 1.0,
             0.5,  0.5,  0.5,  1.0, 1.0,
            -0.5,  0.5,  0.5,  0.0, 1.0,
            -0.5, -0.5,  0.5,  0.0, 0.0,

            -0.5,  0.5,  0.5,  1.0, 0.0,
            -0.5,  0.5, -0.5,  1.0, 1.0,
            -0.5, -0.5, -0.5,  0.0, 1.0,
            -0.5, -0.5, -0.5,  0.0, 1.0,
            -0.5, -0.5,  0.5,  0.0, 0.0,
            -0.5,  0.5,  0.5,  1.0, 0.0,

             0.5,  0.5,  0.5,  1.0, 0.0,
             0.5,  0.5, -0.5,  1.0, 1.0,
             0.5, -0.5, -0.5,  0.0, 1.0,
             0.5, -0.5, -0.5,  0.0, 1.0,
             0.5, -0.5,  0.5,  0.0, 0.0,
             0.5,  0.5,  0.5,  1.0, 0.0,

            -0.5, -0.5, -0.5,  0.0, 1.0,
             0.5, -0.5, -0.5,  1.0, 1.0,
             0.5, -0.5,  0.5,  1.0, 0.0,
             0.5, -0.5,  0.5,  1.0, 0.0,
            -0.5, -0.5,  0.5,  0.0, 0.0,
            -0.5, -0.5, -0.5,  0.0, 1.0,

            -0.5,  0.5, -0.5,  0.0, 1.0,
             0.5,  0.5, -0.5,  1.0, 1.0,
             0.5,  0.5,  0.5,  1.0, 0.0,
             0.5,  0.5,  0.5,  1.0, 0.0,
            -0.5,  0.5,  0.5,  0.0, 0.0,
            -0.5,  0.5, -0.5,  0.0, 1.0
        ]
        vertexBuffer = VertexBuffer(vertices)
        vertexBuffer.layout = BufferLayout([Types.FLOAT3, Types.FLOAT2])
        
        self.vertexArray = VertexArray()
        self.vertexArray.set_vertex_buffer(vertexBuffer)

    def cleanup(self):
        self.shaderTexture.cleanup()
        self.vertexArray.cleanup()

rendererData = None

class Renderer3D():
    @staticmethod
    def init(width, height, clearColor):
        glClearColor(clearColor[0], clearColor[1], clearColor[2], clearColor[3])
        glViewport(0, 0, width, height)
        glEnable(GL_DEPTH_TEST)

        global rendererData
        rendererData = RendererData(width, height)
    
    @staticmethod
    def cleanup():
        rendererData.cleanup()
        
    @staticmethod
    def clear():
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    @staticmethod
    def drawTexturedCube(position, texture, rotation=45.0):
        model = translate(mat4(1.0), vec3(position)) * \
		        rotate(mat4(1.0), radians(rotation), vec3(1.0, 1.0, 0.0)) * \
		        scale(mat4(1.0), vec3(0.5, 0.5, 0.5))
        
        rendererData.shaderTexture.bind()
        rendererData.shaderTexture.set_mat4('model', value_ptr(model))
        
        texture.bind(GL_TEXTURE0)
        
        rendererData.vertexArray.bind()
        glDrawArrays(GL_TRIANGLES, 0, 36)
        texture.unbind()
