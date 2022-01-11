from window import window
from events.event import EventDispatcher
from events.keyboard_events import KeyPressedEvent, KeyCode
from events.window_events import WindowCloseEvent
from graphics.renderer import Renderer
from graphics.camera import Camera

class Application():
    def __init__(self):
        self.isRunning = True
        self.camera = Camera(45.0, window.windowData.width / window.windowData.height, 0.1, 1000.0)
        window.set_event_callback(self.on_event)
        Renderer.init(window.windowData.width, 
                        window.windowData.height, 
                        (0.0, 0.0, 0.0),
                        self.camera,
                        'example_scene')

    def on_event(self, event):
        dispatcher = EventDispatcher(event)
        dispatcher.dispatch(self.on_window_close)
        dispatcher.dispatch(self.on_key_pressed)

        self.camera.on_event(event)

    def on_update(self, timestep):
        self.camera.on_update(timestep)

    def run(self):
        timeSinceLastUpdate = 0.0
        while self.isRunning:
            time = window.get_time()
            timestep = time - timeSinceLastUpdate
            timeSinceLastUpdate = time
            self.on_update(timestep)

            Renderer.clear()

            Renderer.draw_fullscreen_quad()

            window.update()
        
        Renderer.cleanup() 
        window.cleanup()

    def on_window_close(self, windowCloseEvent : WindowCloseEvent):
        self.isRunning = False
        return True

    def on_key_pressed(self, keyPressedEvent : KeyPressedEvent):
        if keyPressedEvent.keyCode == KeyCode.ESC:
            self.isRunning = False
            return True

        if keyPressedEvent.keyCode == KeyCode.RIGHT:
            Renderer.update_reflection_depth(1)
        elif keyPressedEvent.keyCode == KeyCode.LEFT:
            Renderer.update_reflection_depth(-1)

        return False
