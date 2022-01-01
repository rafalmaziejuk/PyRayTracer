from window import window
from events.event import EventDispatcher
from events.keyboard_events import KeyPressedEvent, KeyCode
from events.window_events import WindowCloseEvent
from graphics.renderer3d import Renderer3D
from graphics.texture import Texture
from graphics.camera import Camera

global window

class Application():
    def __init__(self):
        self.isRunning = True
        self.camera = Camera(45.0, window.windowData.width / window.windowData.height, 0.1, 1000.0)
        window.set_event_callback(self.on_event)
        Renderer3D.init(window.windowData.width, 
                        window.windowData.height, 
                        (0.2, 0.3, 0.3, 1.0),
                        self.camera)

    def on_event(self, event):
        dispatcher = EventDispatcher(event)
        dispatcher.dispatch(self.on_window_close)
        dispatcher.dispatch(self.on_key_pressed)

        self.camera.on_event(event)

    def on_update(self, timestep):
        self.camera.on_update(timestep)

    def run(self):
        texture = Texture('block.png')
        timeSinceLastUpdate = 0.0

        while self.isRunning:
            time = window.get_time()
            timestep = time - timeSinceLastUpdate
            timeSinceLastUpdate = time

            self.on_update(timestep)

            Renderer3D.clear()
            Renderer3D.draw_textured_cube(texture, (0.0, 2.0, 0.0), (1.0, 1.0, 1.0))
            Renderer3D.draw_textured_cube(texture, (0.0, -2.0, 0.0), (10.0, 10.0, 0.01), 90.0, (1.0, 0.0, 0.0))

            window.update()
        
        texture.cleanup()
        Renderer3D.cleanup() 
        window.cleanup()

    def on_window_close(self, windowCloseEvent : WindowCloseEvent):
        self.isRunning = False
        return True

    def on_key_pressed(self, keyPressedEvent : KeyPressedEvent):
        if keyPressedEvent.keyCode == KeyCode.ESC:
            self.isRunning = False
            return True

        return False
