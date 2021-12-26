from window import Window
from OpenGL.GL import *

class Application():
    def __init__(self, width=800, height=600, name="PyRayTracer"):
        self.window = Window(width, height, name)

    def run(self):
        while self.window.is_running():
            self.window.process_input()

            glClearColor(0.2, 0.3, 0.3, 1.0);
            glClear(GL_COLOR_BUFFER_BIT);

            self.window.update()

        self.window.cleanup()
