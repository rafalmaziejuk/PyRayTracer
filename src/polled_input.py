from glm import vec2
from glfw.GLFW import (
	GLFW_PRESS, GLFW_REPEAT,
	glfwGetKey, glfwGetCursorPos
)

class Input():
	@staticmethod
	def is_key_pressed(windowHandle, keyCode):
		state = glfwGetKey(windowHandle, keyCode)
		return state == GLFW_PRESS or state == GLFW_REPEAT

	@staticmethod
	def get_mouse_position(windowHandle):
		return vec2(glfwGetCursorPos(windowHandle))
