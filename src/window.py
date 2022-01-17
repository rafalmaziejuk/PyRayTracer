from events.keyboard_events import KeyPressedEvent, KeyReleasedEvent
from events.mouse_events import MouseMovedEvent, MouseButtonPressedEvent, MouseButtonReleasedEvent, MouseScrollEvent
from events.window_events import WindowCloseEvent, WindowResizeEvent
from sys import exit
from glfw.GLFW import (
	GLFW_PRESS, GLFW_RELEASE,
	GLFW_CONTEXT_VERSION_MAJOR, GLFW_CONTEXT_VERSION_MINOR,
	GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE,
	GLFW_CURSOR, GLFW_CURSOR_DISABLED,
	glfwInit, glfwTerminate, 
	glfwCreateWindow, glfwDestroyWindow,
	glfwWindowHint, glfwMakeContextCurrent, glfwSwapInterval, 
	glfwPollEvents, glfwSwapBuffers, glfwGetTime,
	glfwSetWindowUserPointer, glfwGetWindowUserPointer,
	glfwSetWindowCloseCallback, glfwSetWindowSizeCallback,
	glfwSetKeyCallback, 
	glfwSetMouseButtonCallback, glfwSetCursorPosCallback, glfwSetScrollCallback, glfwSetInputMode
)

def window_close_callback(windowHandle):
	data = glfwGetWindowUserPointer(windowHandle)
	data.eventCallback(WindowCloseEvent())

def window_resize_callback(windowHandle, width, height):
	data = glfwGetWindowUserPointer(windowHandle)
	data.width = width
	data.height = height
	data.eventCallback(WindowResizeEvent(width, height))

def window_key_callback(windowHandle, key, scancode, action, mods):
	data = glfwGetWindowUserPointer(windowHandle)

	if action == GLFW_PRESS:
		data.eventCallback(KeyPressedEvent(key))
	elif action == GLFW_RELEASE:
		data.eventCallback(KeyReleasedEvent(key))

def window_mouse_button_callback(windowHandle, button, action, mods):
	data = glfwGetWindowUserPointer(windowHandle)

	if action == GLFW_PRESS:
		data.eventCallback(MouseButtonPressedEvent(button))
	elif action == GLFW_RELEASE:
		data.eventCallback(MouseButtonReleasedEvent(button))

def window_mouse_scroll_callback(windowHandle, x, y):
	data = glfwGetWindowUserPointer(windowHandle)
	data.eventCallback(MouseScrollEvent(x, y))

def window_mouse_moved_callback(windowHandle, x, y):
	data = glfwGetWindowUserPointer(windowHandle)
	data.eventCallback(MouseMovedEvent(x, y))

class WindowData():
	def __init__(self, width, height, name):
		self.width = width
		self.height = height
		self.name = name
		self.windowHandle = None
		self.eventCallback = None

class Window():
	def __init__(self, windowData):
		if not glfwInit():
			exit("Couldn't initialize GLFW properly.")

		glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4)
		glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 5)
		glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)

		windowData.windowHandle = glfwCreateWindow(windowData.width,
													windowData.height,
													windowData.name,
													None, None)
		if not windowData.windowHandle:
			glfwTerminate()
			exit("Couldn't create window.")

		glfwMakeContextCurrent(windowData.windowHandle)
		glfwSwapInterval(1)

		glfwSetWindowUserPointer(windowData.windowHandle, windowData)

		glfwSetWindowCloseCallback(windowData.windowHandle, window_close_callback)
		glfwSetWindowSizeCallback(windowData.windowHandle, window_resize_callback)

		glfwSetKeyCallback(windowData.windowHandle, window_key_callback)

		glfwSetMouseButtonCallback(windowData.windowHandle, window_mouse_button_callback)
		glfwSetCursorPosCallback(windowData.windowHandle, window_mouse_moved_callback)
		glfwSetScrollCallback(windowData.windowHandle, window_mouse_scroll_callback)
		glfwSetInputMode(windowData.windowHandle, GLFW_CURSOR, GLFW_CURSOR_DISABLED)

		self.windowData = windowData

	def cleanup(self):
		glfwDestroyWindow(self.windowData.windowHandle)
		glfwTerminate()

	def set_event_callback(self, eventCallback):
		self.windowData.eventCallback = eventCallback

	def update(self):
		glfwPollEvents()
		glfwSwapBuffers(self.windowData.windowHandle)

	def get_time(self):
		return glfwGetTime()

window = Window(WindowData(1280, 720, 'PyRayTracer'))
