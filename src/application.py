from window import Window
from renderer import Renderer
from texture import Texture

class Application():
    def __init__(self, width=800, height=600, name='PyRayTracer'):
        self.window = Window(width, height, name)
        Renderer.init(width, height, (0.2, 0.3, 0.3, 1.0))

        self.texture = Texture('block.png')

    def run(self):
        while self.window.is_running():
            self.window.process_input()

            Renderer.clear()
            Renderer.drawSolid((200.0, 300.0), (128.0, 128.0), (1.0, 0.5, 0.2), 45.0)
            Renderer.drawTexture((600.0, 300.0), self.texture, 45.0)

            self.window.update()
        
        self.texture.cleanup()
        Renderer.cleanup() 
        self.window.cleanup()
