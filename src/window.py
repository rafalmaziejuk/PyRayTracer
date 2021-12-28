from glfw.GLFW import *

import sys

class Window():
    def __init__(self, width, height, name):
        self.width = width
        self.height = height
        self.name = name

        if not glfwInit():
            sys.exit("Couldn't initialize GLFW properly.")

        glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4)
        glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 5)
        glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)

        self.window_handle = glfwCreateWindow(width, height, name, None, None)
        if not self.window_handle:
            glfwTerminate()
            sys.exit("Couldn't create window.")

        glfwMakeContextCurrent(self.window_handle)
        glfwSwapInterval(1)

    def cleanup(self):
        glfwDestroyWindow(self.window_handle)
        glfwTerminate()

    def update(self):
        glfwPollEvents()
        glfwSwapBuffers(self.window_handle)

    def is_running(self):
        return not glfwWindowShouldClose(self.window_handle)
        
    def process_input(self):
        if glfwGetKey(self.window_handle, GLFW_KEY_ESCAPE) == GLFW_PRESS:
            glfwSetWindowShouldClose(self.window_handle, True)

    def get_time(self):
        return glfwGetTime()
