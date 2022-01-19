from scenes.scene import Scene
from graphics.fullscreen_quad import FullscreenQuad
from graphics.texture import Texture
from glm import tan, acos
from OpenGL.GL import (
    GL_FALSE,
    GL_BUFFER_DATA_SIZE,
    GL_ALL_BARRIER_BITS,
    GL_SHADER_STORAGE_BLOCK, GL_SHADER_STORAGE_BUFFER,
    GL_READ_ONLY, GL_DYNAMIC_DRAW, GL_STATIC_DRAW,
    GLint, GLubyte,
    glBindImageTexture, glShaderStorageBlockBinding, 
    glGenBuffers, glBindBuffer, glBindBufferBase, glBufferData, glDeleteBuffers,
    glGetProgramResourceIndex, glGetProgramResourceiv,
    glMemoryBarrier, glDispatchCompute
)

WORK_GROUP_SIZE = 16

class Raytracer():
    def __init__(self, width, height, camera, shader, sceneName):
        self.fullscreenQuad = FullscreenQuad(Texture(width, height))
        self.computeShader = shader
        self.camera = camera
        self.reflectionDepth = 1
        self.scene = Scene(sceneName)

        self.__initialize_compute_shader(self.computeShader, self.camera, self.fullscreenQuad.renderTexture)

    def cleanup(self):
        glDeleteBuffers(2, self.bufferIDs)
        self.fullscreenQuad.cleanup()

    def __initialize_compute_shader(self, shader, camera, texture):
        glBindImageTexture(0, texture.id, 0, GL_FALSE, 0, GL_READ_ONLY, texture.internalFormat)

        self.__initialize_compute_shader_uniforms(shader, camera, texture)
        self.__initialize_compute_shader_buffers(shader)

    def __initialize_compute_shader_uniforms(self, shader, camera, texture):
        y = tan(camera.fov * acos(-1) / 180.0 / 2.0)
        x = (texture.width * y) / texture.height
        
        shader.bind()
        shader.set_vec3f('camera.position', camera.position)
        shader.set_vec3f('camera.direction', camera.forward)
        shader.set_vec3f('camera.up', camera.up)
        shader.set_vec3f('camera.right', camera.right)
        shader.set_float('camera.tanFovX', x)
        shader.set_float('camera.tanFovY', y)
        shader.set_uint('width', texture.width)
        shader.set_uint('height', texture.height)
        shader.set_uint('reflectionDepth', self.reflectionDepth)

    def __initialize_compute_shader_buffers(self, shader):
        objectsCount, objectsData = self.scene.get_objects_data()
        lightsCount, lightsData = self.scene.get_lights_data()

        shader.set_uint('numberOfObjects', objectsCount)
        shader.set_uint('numberOfLights', lightsCount)
        
        objectsBlockIndex = glGetProgramResourceIndex(shader.id, GL_SHADER_STORAGE_BLOCK, 'ObjectBuffer')
        lightsBlockIndex = glGetProgramResourceIndex(shader.id, GL_SHADER_STORAGE_BLOCK, 'LightBuffer')
        
        objectsBlockSize = GLint()
        lightsBlockSize = GLint()
        glGetProgramResourceiv(shader.id, GL_SHADER_STORAGE_BLOCK, objectsBlockIndex, 1, [GL_BUFFER_DATA_SIZE], 1, None, objectsBlockSize)
        glGetProgramResourceiv(shader.id, GL_SHADER_STORAGE_BLOCK, lightsBlockIndex, 1, [GL_BUFFER_DATA_SIZE], 1, None, lightsBlockSize)

        objectsAlignOffset = objectsBlockSize.value
        lightsAlignOffset = lightsBlockSize.value if lightsBlockSize.value % 16 == 0 else lightsBlockSize.value - (lightsBlockSize.value % 16) + 16
        
        self.bufferIDs = glGenBuffers(2)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 0, self.bufferIDs[0])
        glBufferData(GL_SHADER_STORAGE_BUFFER, objectsCount * objectsAlignOffset, (GLubyte * (objectsCount * objectsAlignOffset))(*objectsData), GL_DYNAMIC_DRAW)
        glShaderStorageBlockBinding(shader.id, objectsBlockIndex, 0)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)

        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 1, self.bufferIDs[1])
        glBufferData(GL_SHADER_STORAGE_BUFFER, lightsCount * lightsAlignOffset, (GLubyte * (lightsCount * lightsAlignOffset))(*lightsData), GL_STATIC_DRAW)
        glShaderStorageBlockBinding(shader.id, lightsBlockIndex, 1)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)

    def update_reflection_depth(self, value):
        changed = False
        if self.reflectionDepth > 1 and value == -1:
            self.reflectionDepth += value
            changed = True
        elif self.reflectionDepth < 5 and value == 1:
            self.reflectionDepth += value
            changed = True

        if changed:    
            self.computeShader.bind()
            self.computeShader.set_uint('reflectionDepth', self.reflectionDepth)

    def raytrace_scene(self):
        self.computeShader.bind()

        self.computeShader.set_vec3f('camera.position', self.camera.position)
        self.computeShader.set_vec3f('camera.direction', self.camera.forward)
        self.computeShader.set_vec3f('camera.up', self.camera.up)
        self.computeShader.set_vec3f('camera.right', self.camera.right)

        glMemoryBarrier(GL_ALL_BARRIER_BITS)
        glDispatchCompute(int(self.fullscreenQuad.renderTexture.width / WORK_GROUP_SIZE),
                          int(self.fullscreenQuad.renderTexture.height / WORK_GROUP_SIZE), 
                          1)
        glMemoryBarrier(GL_ALL_BARRIER_BITS)

    def resize_fullscreen_quad(self, width, height):
        self.computeShader.bind()
        
        y = tan(self.camera.fov * acos(-1) / 180.0 / 2.0)
        x = (width * y) / height
        self.computeShader.set_float('camera.tanFovX', x)
        self.computeShader.set_float('camera.tanFovY', y)

        self.fullscreenQuad.resize(width, height)
        self.computeShader.set_uint('width', width)
        self.computeShader.set_uint('height', height)
