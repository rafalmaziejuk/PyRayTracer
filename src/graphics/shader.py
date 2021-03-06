from glm import value_ptr
from sys import exit
from OpenGL.GL import (
	GL_COMPUTE_SHADER, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER,
	GL_COMPILE_STATUS, GL_LINK_STATUS,
	GLuint, GL_FALSE,
	glCreateProgram, glDeleteProgram, glLinkProgram, glUseProgram,
	glGetProgramiv, glGetProgramInfoLog,
	glCreateShader, glDeleteShader, glAttachShader, glDetachShader,
	glShaderSource, glCompileShader, 
	glGetShaderiv, glGetShaderInfoLog,
	glGetUniformLocation, glUniform1i, glUniform1ui, glUniform1f, glUniform3f, glUniformMatrix4fv
)

def read_file(filepath):
	with open(filepath, 'r') as sourceFile:
		source = sourceFile.readlines()

	return source

class Shader():
	def __init__(self, filename):
		self.id = glCreateProgram()
		source = read_file(filename)
		shaderSources = {}
		
		try:
			foundComp = source.index('#type compute\n')
			shaderSources[GL_COMPUTE_SHADER] = source[1:]
		except ValueError as VE:
			try:
				foundVert = source.index('#type vertex\n')
				foundFrag = source.index('#type fragment\n')
			
				shaderSources[GL_VERTEX_SHADER] = source[foundVert + 1:foundFrag - 1]
				shaderSources[GL_FRAGMENT_SHADER] = source[foundFrag + 1:]
			except ValueError as VE:
				print(f"{filename} is not a valid shader file.")
				return

		self.__compile(shaderSources)

	def cleanup(self):
		glDeleteProgram(self.id)

	def __compile(self, shaderSources):
		shaders = []
		for shaderType, shaderSource in shaderSources.items():
			shader = glCreateShader(shaderType)
			glShaderSource(shader, shaderSource)
			glCompileShader(shader)
			
			retVal = GLuint()
			glGetShaderiv(shader, GL_COMPILE_STATUS, retVal)
			if not retVal:
				log = glGetShaderInfoLog(shader).decode('utf-8')
				glDeleteShader(shader)
				exit("Couldn't compile shader properly.\n" + log)

			glAttachShader(self.id, shader)
			shaders.append(shader)
		
		glLinkProgram(self.id)

		for shader in shaders:
			glDetachShader(self.id, shader)
			glDeleteShader(shader)
		
		retVal = GLuint()
		glGetProgramiv(self.id, GL_LINK_STATUS, retVal)
		if not retVal:
			log = glGetProgramInfoLog(self.id).decode('utf-8')
			glDeleteProgram(self.id)
			exit("Couldn't link shader program.\n" + log)

	def bind(self):
		glUseProgram(self.id)

	def set_int(self, name, value):
		location = glGetUniformLocation(self.id, name)
		glUniform1i(location, value)

	def set_uint(self, name, value):
		location = glGetUniformLocation(self.id, name)
		glUniform1ui(location, value)

	def set_float(self, name, value):
		location = glGetUniformLocation(self.id, name)
		glUniform1f(location, value)
	
	def set_vec3f(self, name, vec):
		location = glGetUniformLocation(self.id, name)
		glUniform3f(location, vec.x, vec.y, vec.z)
	
	def set_mat4(self, name, matrix):
		location = glGetUniformLocation(self.id, name)
		glUniformMatrix4fv(location, 1, GL_FALSE, value_ptr(matrix))
