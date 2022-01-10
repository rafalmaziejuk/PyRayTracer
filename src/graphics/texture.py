from OpenGL.GL import *
from PIL import Image
from os import path
from ctypes import pointer, c_uint

class Texture():
	def __init__(self, width=None, height=None, filename=None):
		self.id = c_uint()
		self.width = None
		self.height = None
		self.size = None
		self.internalFormat = None
		self.dataFormat = None

		if width and height:
			self.__create_texture(width, height)

		if filename:
			self.__load_texture(filename)

	def cleanup(self):
		glDeleteTextures(1, self.id)

	def __create_texture(self, width, height):
		self.width = width
		self.height = height
		self.internalFormat = GL_RGBA8
		self.dataFormat = GL_RGBA

		glCreateTextures(GL_TEXTURE_2D, 1, pointer(self.id))
		glBindTexture(GL_TEXTURE_2D, self.id)
		glTexImage2D(GL_TEXTURE_2D, 0, self.internalFormat, self.width, self.height, 0, self.dataFormat, GL_UNSIGNED_BYTE, None)

		glTextureParameteri(self.id, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		glTextureParameteri(self.id, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTextureParameteri(self.id, GL_TEXTURE_WRAP_S, GL_REPEAT)
		glTextureParameteri(self.id, GL_TEXTURE_WRAP_T, GL_REPEAT)

	def __load_texture(self, filename):
		image = Image.open(path.join('../textures/', filename)).transpose(Image.FLIP_TOP_BOTTOM)
		bytess = image.tobytes()
		self.width = image.width
		self.height = image.height
		self.size = image.size

		if image.mode == 'RGB':
			self.internalFormat = GL_RGB8
			self.dataFormat = GL_RGB
		elif image.mode == 'RGBA':
			self.internalFormat = GL_RGBA8
			self.dataFormat = GL_RGBA

		glCreateTextures(GL_TEXTURE_2D, 1, pointer(self.id))
		glTextureStorage2D(self.id, 1, self.internalFormat, self.width, self.height)

		glTextureParameteri(self.id, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		glTextureParameteri(self.id, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTextureParameteri(self.id, GL_TEXTURE_WRAP_S, GL_REPEAT)
		glTextureParameteri(self.id, GL_TEXTURE_WRAP_T, GL_REPEAT)

		glTextureSubImage2D(self.id, 0, 0, 0, self.width, self.height, self.dataFormat, GL_UNSIGNED_BYTE, image.tobytes())
		glGenerateMipmap(GL_TEXTURE_2D)

	def bind(self, slot=0):
		glBindTextureUnit(slot, self.id)
