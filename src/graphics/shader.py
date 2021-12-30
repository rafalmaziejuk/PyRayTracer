from OpenGL.GL import *

def read_file(filepath):
	with open(filepath, 'r') as sourceFile:
		source = sourceFile.readlines()

	return source

class Shader():
	def __init__(self, vert, frag):
		self.id = glCreateProgram()

		shaderSources = {
			GL_VERTEX_SHADER:   read_file(vert),
			GL_FRAGMENT_SHADER: read_file(frag)
			}

		self.__compile(shaderSources)

	def cleanup(self):
		glDeleteProgram(self.id)

	def __compile(self, shaderSources):
		shaders = []
		for shaderType, shaderSource in shaderSources.items():
			shader = glCreateShader(shaderType)
			glShaderSource(shader, shaderSource)
			glCompileShader(shader)
			glAttachShader(self.id, shader)

			shaders.append(shader)
		
		glLinkProgram(self.id)

		for shader in shaders:
			glDetachShader(self.id, shader)
			glDeleteShader(shader)

	def bind(self):
		glUseProgram(self.id)

	def set_int(self, name, value):
		location = glGetUniformLocation(self.id, name)
		glUniform1i(location, value)
	
	def set_float(self, name, value):
		location = glGetUniformLocation(self.id, name)
		glUniform1f(location, value)
	
	def set_vec3f(self, name, vec):
		location = glGetUniformLocation(self.id, name)
		glUniform3f(location, vec.x, vec.y, vec.z)
	
	def set_mat4 (self, name, matrix):
		location = glGetUniformLocation(self.id, name)
		glUniformMatrix4fv(location, 1, GL_FALSE, matrix)
