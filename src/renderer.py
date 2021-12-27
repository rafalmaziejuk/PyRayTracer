from OpenGL.GL import *

class Renderer():
    @staticmethod
    def clear():
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
