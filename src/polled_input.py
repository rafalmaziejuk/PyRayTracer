from glfw.GLFW import glfwGetKey, glfwGetCursorPos, GLFW_PRESS, GLFW_REPEAT
from glm import vec2

class Input():
	@staticmethod
	def is_key_pressed(windowHandle, keyCode):
		state = glfwGetKey(windowHandle, keyCode)
		return state == GLFW_PRESS or state == GLFW_REPEAT

	@staticmethod
	def get_mouse_position(windowHandle):
		return vec2(glfwGetCursorPos(windowHandle))
