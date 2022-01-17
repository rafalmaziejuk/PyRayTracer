from ctypes import c_void_p
from OpenGL.GL import (
	GL_FLOAT, GL_FALSE,
	glGenVertexArrays, glBindVertexArray, glDeleteVertexArrays,
	glEnableVertexAttribArray, glVertexAttribPointer
)

class VertexArray():
	def __init__(self):
		self.id = glGenVertexArrays(1)
		self.vertexBuffer = None
		self.elementBuffer = None

	def cleanup(self):
		self.vertexBuffer.cleanup()
		if self.elementBuffer:
			self.elementBuffer.cleanup()
		glDeleteVertexArrays(1, [self.id])

	def bind(self):
		glBindVertexArray(self.id)

	def unbind(self):
		glBindVertexArray(0)

	def set_vertex_buffer(self, vertexBuffer):
		self.bind()
		vertexBuffer.bind()

		#Iterate through layout's vertex buffer elements
		stride = vertexBuffer.layout.stride
		for i, element in enumerate(vertexBuffer.layout.vbElements):
			glEnableVertexAttribArray(i)
			glVertexAttribPointer(
				i, 
				element.dataType,
				GL_FLOAT,
				GL_FALSE,
				stride,
				c_void_p(element.offset))

		self.vertexBuffer = vertexBuffer

	def set_element_buffer(self, elementBuffer):
		self.bind()
		elementBuffer.bind()
		self.elementBuffer = elementBuffer
