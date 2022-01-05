from graphics.shader import Shader
from os import listdir

PATH = 'shaders/'
EXTENSION = '.glsl'

class ShaderLibrary():
    def __init__(self):
        self.library = {}

        shaderFilenames = [PATH + name for name in listdir(PATH) if EXTENSION in name]
        shaderNames = [name[len(PATH):-len(EXTENSION)] for name in shaderFilenames]

        for shaderName, filename in zip(shaderNames, shaderFilenames):
            self.library[shaderName] = Shader(filename)

    def __getitem__(self, key):
        self.library[key].bind()
        return self.library[key]

    def cleanup(self):
        for shader in self.library.values():
            shader.cleanup()

    def values(self):
        return self.library.values()
