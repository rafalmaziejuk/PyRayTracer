from OpenGL.GL import *
from os import path
from PIL import Image

class Texture():
	def __init__(self, filename):
		image = self.__load_image(filename)
		self.width = image.width
		self.height = image.height
		self.size = image.size

		self.id = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, self.id)

		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

		internalFormat = 0
		dataFormat = 0
		if image.mode == 'RGB':
			internalFormat = GL_RGB8
			dataFormat = GL_RGB
		elif image.mode == 'RGBA':
			internalFormat = GL_RGBA8
			dataFormat = GL_RGBA

		glTexImage2D(GL_TEXTURE_2D, 0, internalFormat, self.width, self.height, 0, dataFormat, GL_UNSIGNED_BYTE, image.tobytes())
		glGenerateMipmap(GL_TEXTURE_2D)

	def cleanup(self):
		glDeleteTextures(1, [self.id])

	def __load_image(self, filename):
		return Image.open(path.join('../textures/', filename)).transpose(Image.FLIP_TOP_BOTTOM)

	def bind(self, slot):
		glActiveTexture(slot)
		glBindTexture(GL_TEXTURE_2D, self.id)

	def unbind(self):
		glBindTexture(GL_TEXTURE_2D, 0)
