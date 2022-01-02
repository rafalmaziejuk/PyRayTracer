from graphics.shader import Shader
from OpenGL.GL import *
from glm import value_ptr, vec3
from enum import IntEnum

class RenderingMode(IntEnum):
    LINES = GL_LINES,
    TRIANGLES = GL_TRIANGLES

class RendererData():
    def __init__(self, width, height, camera):
        self.camera = camera
        self.width = width
        self.height = height
        
        self.shaderTexture = Shader('shaders/texture.vert', 'shaders/texture.frag')
        self.shaderTexture.bind()
        self.shaderTexture.set_int('texture0', 0)
        self.shaderTexture.set_mat4('projection', value_ptr(camera.get_projection_matrix()))
        
        self.shaderFlatColor = Shader('shaders/flat_color.vert', 'shaders/flat_color.frag')
        self.shaderFlatColor.bind()
        self.shaderFlatColor.set_mat4('projection', value_ptr(camera.get_projection_matrix()))


    def cleanup(self):
        self.shaderTexture.cleanup()
        self.shaderFlatColor.cleanup()

rendererData = None

class Renderer3D():
    @staticmethod
    def init(width, height, clearColor, camera):
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LINE_SMOOTH)
        glViewport(0, 0, width, height)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(clearColor[0], clearColor[1], clearColor[2], 1.0)

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

        rendererData.shaderFlatColor.bind()
        rendererData.shaderFlatColor.set_mat4('projection', value_ptr(projectionMatrix))

    @staticmethod
    def draw_colored(mesh, mode=RenderingMode.TRIANGLES):
        rendererData.shaderFlatColor.bind()
        rendererData.shaderFlatColor.set_vec3f('uColor', vec3(mesh.color))
        rendererData.shaderFlatColor.set_mat4('model', value_ptr(mesh.modelMatrix))
        rendererData.shaderFlatColor.set_mat4('view', value_ptr(rendererData.camera.get_view_matrix()))
        
        mesh.bind()
        glDrawElements(mode, mesh.vertexArray.elementBuffer.elementCount, GL_UNSIGNED_INT, None)
        mesh.unbind()

    @staticmethod
    def draw_textured(mesh, mode=RenderingMode.TRIANGLES):
        rendererData.shaderTexture.bind()
        rendererData.shaderTexture.set_mat4('model', value_ptr(mesh.modelMatrix))
        rendererData.shaderTexture.set_mat4('view', value_ptr(rendererData.camera.get_view_matrix()))
        
        mesh.bind(GL_TEXTURE0)
        glDrawElements(mode, mesh.vertexArray.elementBuffer.elementCount, GL_UNSIGNED_INT, None)
        mesh.unbind()
