from window import Window
from renderer import Renderer

class Application():
    def __init__(self, width=800, height=600, name='PyRayTracer'):
        self.window = Window(width, height, name)
        Renderer.init(width, height, (0.2, 0.3, 0.3, 1.0))

    def run(self):
        while self.window.is_running():
            self.window.process_input()

            Renderer.clear()
            Renderer.draw((400.0, 300.0), (100.0, 100.0), (1.0, 0.5, 0.2))

            self.window.update()
        
        Renderer.cleanup() 
        self.window.cleanup()
