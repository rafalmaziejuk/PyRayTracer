from graphics.fullscreen_quad import FullscreenQuad
from graphics.texture import Texture
from OpenGL.GL import *
from glm import tan, acos, vec2, vec3, vec4

from enum import IntEnum
from struct import pack

WORK_GROUP_SIZE = 16

class ObjectTypes(IntEnum):
    SPHERE = 1,
    PLANE = 2,
    TRIANGLE = 3

class LightTypes(IntEnum):
    POINT = 1,
    DIRECTIONAL = 2

class Object():
    def __init__(self, objectType, position, colour, data1, data2, data3):
        position = vec3(position)
        colour = vec4(colour, 1.0)

        self.bytesArray = bytearray()
        self.bytesArray.extend(pack("f", position.x))
        self.bytesArray.extend(pack("f", position.y))
        self.bytesArray.extend(pack("f", position.z))
        self.bytesArray.extend(pack("i", objectType))

        self.bytesArray.extend(pack("f", colour.x))
        self.bytesArray.extend(pack("f", colour.y))
        self.bytesArray.extend(pack("f", colour.z))
        self.bytesArray.extend(pack("f", colour.w))

        self.bytesArray.extend(pack("f", data1.x))
        self.bytesArray.extend(pack("f", data1.y))
        self.bytesArray.extend(pack("f", data1.z))
        self.bytesArray.extend(pack("f", data1.w))

        self.bytesArray.extend(pack("f", data2.x))
        self.bytesArray.extend(pack("f", data2.y))
        self.bytesArray.extend(pack("f", data2.z))
        self.bytesArray.extend(pack("f", data2.w))

        self.bytesArray.extend(pack("f", data3.x))
        self.bytesArray.extend(pack("f", data3.y))
        self.bytesArray.extend(pack("f", data3.z))
        self.bytesArray.extend(pack("f", data3.w))

class Sphere(Object):
    def __init__(self, position, radius, colour=(1.0, 1.0, 1.0)):
        data1 = vec4(radius, vec3(0.0))
        data2 = vec4(0.0)
        data3 = vec4(0.0)

        super().__init__(ObjectTypes.SPHERE, position, colour, data1, data2, data3)

class Plane(Object):
    def __init__(self, position, size, colour=(1.0, 1.0, 1.0)):
        data1 = vec4(vec3(0.0, 1.0, 0.0), 0.0)
        data2 = vec4(vec2(size), vec2(0.0))
        data3 = vec4(0.0)

        super().__init__(ObjectTypes.PLANE, position, colour, data1, data2, data3)

class Triangle(Object):
    def __init__(self, position, size, A, B, C, colour=(1.0, 1.0, 1.0)):
        A = vec3(A) * size
        B = vec3(B) * size
        C = vec3(C) * size

        data1 = vec4(A, 0.0)
        data2 = vec4(B, 0.0)
        data3 = vec4(C, 0.0)

        super().__init__(ObjectTypes.TRIANGLE, position, colour, data1, data2, data3)

class Cube():
    def __init__(self, position, size, colour=(1.0, 1.0, 1.0)):
        self.triangles = [
            # left
            Triangle(position, size, (-0.5, -0.5,  0.5), (-0.5,  0.5, -0.5), (-0.5, -0.5, -0.5), colour),
            Triangle(position, size, (-0.5, -0.5,  0.5), (-0.5,  0.5,  0.5), (-0.5,  0.5, -0.5), colour),
                                                                                               
            #front                                                                             
            Triangle(position, size, (-0.5, -0.5,  0.5), ( 0.5,  0.5,  0.5), (-0.5,  0.5,  0.5), colour),
            Triangle(position, size, (-0.5, -0.5,  0.5), ( 0.5, -0.5,  0.5), ( 0.5,  0.5,  0.5), colour),
                                                                                               
            # back                                                                             
            Triangle(position, size, ( 0.5, -0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5,  0.5, -0.5), colour),
            Triangle(position, size, ( 0.5, -0.5, -0.5), (-0.5,  0.5, -0.5), ( 0.5,  0.5, -0.5), colour),
                                                                                               
            # right                                                                            
            Triangle(position, size, ( 0.5, -0.5,  0.5), ( 0.5, -0.5, -0.5), ( 0.5,  0.5, -0.5), colour),
            Triangle(position, size, ( 0.5,  0.5, -0.5), ( 0.5,  0.5,  0.5), ( 0.5, -0.5,  0.5), colour),
                                                                                               
            # top                                                                              
            Triangle(position, size, ( 0.5,  0.5, -0.5), (-0.5,  0.5, -0.5), (-0.5,  0.5,  0.5), colour),
            Triangle(position, size, ( 0.5,  0.5, -0.5), (-0.5,  0.5,  0.5), ( 0.5,  0.5,  0.5), colour),
                                                                                               
            # bottom                                                                           
            Triangle(position, size, ( 0.5, -0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, -0.5,  0.5), colour),
            Triangle(position, size, ( 0.5, -0.5, -0.5), (-0.5, -0.5,  0.5), ( 0.5, -0.5,  0.5), colour),
            ]

class Light():
    def __init__(self, position, colour, attenuation, lightType):
        self.position = position
        self.colour = colour
        self.attenuation = attenuation
        self.lightType = lightType
        
        self.bytesArray = bytearray()
        self.bytesArray.extend(pack("f", self.position.x))
        self.bytesArray.extend(pack("f", self.position.y))
        self.bytesArray.extend(pack("f", self.position.z))
        self.bytesArray.extend(pack("f", 0.0)) #padding
        self.bytesArray.extend(pack("f", self.colour.x))
        self.bytesArray.extend(pack("f", self.colour.y))
        self.bytesArray.extend(pack("f", self.colour.z))
        self.bytesArray.extend(pack("f", 0.0)) #padding
        self.bytesArray.extend(pack("f", self.attenuation.x))
        self.bytesArray.extend(pack("f", self.attenuation.y))
        self.bytesArray.extend(pack("f", self.attenuation.z))
        self.bytesArray.extend(pack("i", self.lightType))

class Raytracer():
    def __init__(self, width, height, camera, shader):
        self.fullscreenQuad = FullscreenQuad(Texture(width, height))
        self.computeShader = shader
        self.camera = camera
        self.reflectionDepth = 3

        self.__initialize_compute_shader(self.computeShader, self.camera, self.fullscreenQuad.renderTexture)

    def cleanup(self):
        glDeleteBuffers(2, self.bufferIDs)
        self.fullscreenQuad.cleanup()

    def __initialize_compute_shader(self, shader, camera, texture):
        glBindImageTexture(0, texture.id, 0, GL_FALSE, 0, GL_READ_WRITE, texture.internalFormat)

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
        objects = [
            Sphere((-7.5,   2.5,   0.0), 1.0),
            Sphere(( 7.5,   2.5,   0.0), 1.0),
            Sphere((  0.0,  2.5,  7.5),  1.0),
            Sphere((  0.0,  2.5, -7.5),  1.0),
            Sphere((  0.0,  7.5,   0.0), 1.0),
            Plane((0.0, 0.0, 0.0), (30.0, 30.0)),
            ]

        cube = Cube((0.0, 3.0, 0.0), 6.0)
        objects.extend(cube.triangles)
        
        objectsData = bytearray()
        for obj in objects:
            objectsData.extend(obj.bytesArray)

        lights = [
            Light(vec3(   0.0, 20.0,    0.0), vec3(1.0, 1.0, 1.0), vec3(0.0, 0.0, 0.5), LightTypes.POINT),
            Light(vec3(  10.0, 10.0,    0.0), vec3(1.0, 1.0, 1.0), vec3(0.0, 0.0, 3.0), LightTypes.POINT),
            Light(vec3( -10.0, 10.0,    0.0), vec3(1.0, 1.0, 1.0), vec3(0.0, 0.0, 3.0), LightTypes.POINT),
            Light(vec3(   0.0, 10.0,   10.0), vec3(1.0, 1.0, 1.0), vec3(0.0, 0.0, 3.0), LightTypes.POINT),
            Light(vec3(   0.0, 10.0,  -10.0), vec3(1.0, 1.0, 1.0), vec3(0.0, 0.0, 3.0), LightTypes.POINT),
            ]

        lightsData = bytearray()
        for light in lights:
            lightsData.extend(light.bytesArray)

        shader.set_uint('numberOfObjects', len(objects))
        shader.set_uint('numberOfLights', len(lights))
        
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
        glBufferData(GL_SHADER_STORAGE_BUFFER, len(objects) * objectsAlignOffset, (GLubyte * (len(objects) * objectsAlignOffset))(*objectsData), GL_DYNAMIC_DRAW)
        glShaderStorageBlockBinding(shader.id, objectsBlockIndex, 0)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)

        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 1, self.bufferIDs[1])
        glBufferData(GL_SHADER_STORAGE_BUFFER, len(lights) * lightsAlignOffset, (GLubyte * (len(lights) * lightsAlignOffset))(*lightsData), GL_STATIC_DRAW)
        glShaderStorageBlockBinding(shader.id, lightsBlockIndex, 1)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)

    def raytrace_scene(self):
        self.computeShader.bind()

        self.computeShader.set_vec3f('camera.position', self.camera.position)
        self.computeShader.set_vec3f('camera.direction', self.camera.forward)
        self.computeShader.set_vec3f('camera.up', self.camera.up)
        self.computeShader.set_vec3f('camera.right', self.camera.right)
        
        glMemoryBarrier(GL_ALL_BARRIER_BITS)
        glDispatchCompute(int(self.fullscreenQuad.renderTexture.width / 16),
                          int(self.fullscreenQuad.renderTexture.height / 16), 
                          1)
        glMemoryBarrier(GL_ALL_BARRIER_BITS)

    def update_reflection_depth(self, value):
        self.computeShader.bind()
        self.computeShader.set_uint('reflectionDepth', self.reflectionDepth + value)

    def resize_fullscreen_quad(self, width, height):
        self.computeShader.bind()
        self.computeShader.set_uint('width', width)
        self.computeShader.set_uint('height', height)
        self.fullscreenQuad.resize(width, height)
