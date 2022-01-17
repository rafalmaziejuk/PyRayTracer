from graphics.shader_library import ShaderLibrary
from graphics.fullscreen_quad import FullscreenQuad
from graphics.raytracer import Raytracer
from enum import IntEnum
from OpenGL.GL import (
     GL_LINES, GL_TRIANGLES, GL_TRIANGLE_STRIP,
     GL_BLEND, GL_DEPTH_TEST, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA,
     GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT,
     GL_UNSIGNED_INT,
     glEnable, glViewport, 
     glBlendFunc, glClearColor, glClear,
     glDrawElements, glDrawArrays
)

class RenderingMode(IntEnum):
    LINES = GL_LINES,
    TRIANGLES = GL_TRIANGLES

class RendererData():
    def __init__(self, width, height, camera, sceneName):
        self.camera = camera
        self.width = width
        self.height = height

        self.shaderLibrary = ShaderLibrary()
        
        self.shaderLibrary['flat_color'].set_mat4('projection', camera.get_projection_matrix())
        
        self.shaderLibrary['light'].set_mat4('projection', camera.get_projection_matrix())
        
        self.shaderLibrary['texture'].set_int('texture0', 0)
        self.shaderLibrary['texture'].set_mat4('projection', camera.get_projection_matrix())
        
        self.shaderLibrary['fullscreen_quad'].set_int('texture0', 0)
        self.raytracer = Raytracer(width, height, camera, self.shaderLibrary['ray_tracing'], sceneName)

    def cleanup(self):
        self.shaderLibrary.cleanup()
        self.raytracer.cleanup()

rendererData = None

class Renderer():
    @staticmethod
    def init(width, height, clearColor, camera, sceneName):
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(clearColor[0], clearColor[1], clearColor[2], 1.0)

        global rendererData
        rendererData = RendererData(width, height, camera, sceneName)
    
    @staticmethod
    def cleanup():
        rendererData.cleanup()
        
    @staticmethod
    def clear():
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    @staticmethod
    def update_viewport(width, height):
        glViewport(0, 0, width, height)
        rendererData.raytracer.resize_fullscreen_quad(width, height)

    @staticmethod
    def update_reflection_depth(value):
        rendererData.raytracer.update_reflection_depth(value)

    @staticmethod
    def draw_colored(mesh, mode=RenderingMode.TRIANGLES):
        shader = rendererData.shaderLibrary['flat_color']
        shader.set_vec3f('uMeshColour', mesh.colour)
        shader.set_mat4('model', mesh.modelMatrix)
        shader.set_mat4('view', rendererData.camera.get_view_matrix())
        
        mesh.bind()
        glDrawElements(mode, mesh.vertexArray.elementBuffer.elementCount, GL_UNSIGNED_INT, None)
        mesh.unbind()

    @staticmethod
    def draw_illuminated(mesh, lightSource, mode=RenderingMode.TRIANGLES):
        shader = rendererData.shaderLibrary['light']
        shader.set_vec3f('uMeshColour', mesh.colour)
        shader.set_vec3f('uCameraPosition', rendererData.camera.position)
        shader.set_mat4('model', mesh.modelMatrix)
        shader.set_mat4('view', rendererData.camera.get_view_matrix())
        lightSource.set_light_uniform(shader)
        
        mesh.bind()
        glDrawElements(mode, mesh.vertexArray.elementBuffer.elementCount, GL_UNSIGNED_INT, None)
        mesh.unbind()

    @staticmethod
    def draw_textured(mesh, mode=RenderingMode.TRIANGLES):
        shader = rendererData.shaderLibrary['texture']
        shader.set_mat4('model', mesh.modelMatrix)
        shader.set_mat4('view', rendererData.camera.get_view_matrix())
        
        mesh.bind()
        glDrawElements(mode, mesh.vertexArray.elementBuffer.elementCount, GL_UNSIGNED_INT, None)
        mesh.unbind()

    @staticmethod
    def draw_fullscreen_quad():
        rendererData.raytracer.raytrace_scene()

        shader = rendererData.shaderLibrary['fullscreen_quad']
        rendererData.raytracer.fullscreenQuad.bind()
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        rendererData.raytracer.fullscreenQuad.unbind()
