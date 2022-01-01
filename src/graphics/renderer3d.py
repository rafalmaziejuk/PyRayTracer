from graphics.vertex_array import VertexArray
from graphics.vertex_buffer import VertexBuffer, BufferLayout, Types
from graphics.shader import Shader
from OpenGL.GL import *
from glm import value_ptr, perspective, translate, rotate, radians, scale, mat4, vec3

class RendererData():
    def __init__(self, width, height, camera):
        self.camera = camera
        self.width = width
        self.height = height
        self.shaderTexture = Shader('shaders/shaderTexture3D.vert', 'shaders/shaderTexture3D.frag')
        self.shaderTexture.bind()
        self.shaderTexture.set_int('texture0', 0)
        self.shaderTexture.set_mat4('projection', value_ptr(camera.get_projection_matrix()))
		
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
    def init(width, height, clearColor, camera):
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(clearColor[0], clearColor[1], clearColor[2], clearColor[3])

        global rendererData
        rendererData = RendererData(width, height, camera)
    
    @staticmethod
    def cleanup():
        rendererData.cleanup()
        
    @staticmethod
    def clear():
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    @staticmethod
    def update_viewport(width, height):
        glViewport(0, 0, width, height)

    @staticmethod
    def update_projection_matrix(projectionMatrix):
        rendererData.shaderTexture.bind()
        rendererData.shaderTexture.set_mat4('projection', value_ptr(projectionMatrix))

    @staticmethod
    def draw_textured_cube(texture, position, size, rotation=0.0, rotationVector=(1.0, 1.0, 1.0)):
        view = rendererData.camera.get_view_matrix()
        model = translate(mat4(1.0), vec3(position)) * \
		        rotate(mat4(1.0), radians(rotation), vec3(rotationVector)) * \
                scale(mat4(1.0), vec3(size))
        
        rendererData.shaderTexture.bind()
        rendererData.shaderTexture.set_mat4('view', value_ptr(view))
        rendererData.shaderTexture.set_mat4('model', value_ptr(model))
        
        texture.bind(GL_TEXTURE0)
        
        rendererData.vertexArray.bind()
        glDrawArrays(GL_TRIANGLES, 0, 36)
        texture.unbind()
