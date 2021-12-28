from window import Window
from renderer3d import Renderer3D
from texture import Texture

class Application():
    def __init__(self, width=800, height=600, name='PyRayTracer'):
        self.window = Window(width, height, name)
        Renderer3D.init(width, height, (0.2, 0.3, 0.3, 1.0))

        self.texture = Texture('block.png')

    def run(self):
        timeSinceLastUpdate = 0.0
        while self.window.is_running():
            time = self.window.get_time()
            timestep = time - timeSinceLastUpdate
            timeSinceLastUpdate = time

            self.window.process_input()

            Renderer3D.clear()
            Renderer3D.drawTexturedCube((0.0, 0.0, 0.0), self.texture, 45.0)

            self.window.update()
        
        self.texture.cleanup()
        Renderer3D.cleanup() 
        self.window.cleanup()
