from OpenGL.GL import *
from enum import IntEnum
from ctypes import sizeof, c_float, c_uint32

class Types(IntEnum) :
	NONE = 0,
	FLOAT = 1,
	FLOAT2 = 2,
	FLOAT3 = 3,
	FLOAT4 = 4

def get_type_size(dataType):
	if dataType == Types.FLOAT:  
		return 1 * sizeof(c_float)
	elif dataType == Types.FLOAT2: 
		return 2 * sizeof(c_float)
	elif dataType == Types.FLOAT3: 
		return 3 * sizeof(c_float)
	elif dataType == Types.FLOAT4: 
		return 4 * sizeof(c_float)

	return 0

class VBElement():
	def __init__(self, dataType):
		self.size = get_type_size(dataType)
		self.dataType = dataType
		self.offset = 0

class BufferLayout():
	def __init__(self, vbElements):
		self.stride = 0
		self.vbElements = []
		for element in vbElements:
			self.vbElements.append(VBElement(element))

		self.calculate_stride()

	def calculate_stride(self):
		offset = 0;
		for element in self.vbElements:
			element.offset = offset
			self.stride += element.size
			offset += element.size

	def __getitem__(self, index):
		return self.vbElements[index]

class VertexBuffer():
	def __init__(self, data):
		self.layout = []
		self.id = glGenBuffers(1)
		glBindBuffer(GL_ARRAY_BUFFER, self.id)
		glBufferData(GL_ARRAY_BUFFER, sizeof(c_float) * len(data), (c_float * len(data))(*data), GL_STATIC_DRAW)

	def cleanup(self):
		glDeleteBuffers(1, [self.id])

	def bind(self):
		glBindBuffer(GL_ARRAY_BUFFER, self.id)

class ElementBuffer():
	def __init__(self, data):
		self.elementCount = len(data)
		self.id = glGenBuffers(1)
		glBindBuffer(GL_ARRAY_BUFFER, self.id);
		glBufferData(GL_ARRAY_BUFFER, sizeof(c_uint32) * self.elementCount, (c_uint32 * len(data))(*data), GL_STATIC_DRAW)

	def cleanup(self):
		glDeleteBuffers(1, [self.id])
		
	def bind(self):
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.id)
