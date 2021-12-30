from window import Window, WindowData
from events.event import EventDispatcher
from events.keyboard_events import KeyPressedEvent, KeyCode
from events.mouse_events import MouseMovedEvent, MouseButtonPressedEvent, MouseCode
from events.window_events import WindowCloseEvent, WindowResizeEvent
from graphics.renderer3d import Renderer3D
from graphics.texture import Texture

class Application():
    def __init__(self):
        self.isRunning = True
        self.window = Window(WindowData(1280, 720, 'PyRayTracer', self.on_event))
        Renderer3D.init(self.window.windowData.width, 
                        self.window.windowData.height, 
                        (0.2, 0.3, 0.3, 1.0))

        self.texture = Texture('block.png')

    def on_window_close(self, windowCloseEvent : WindowCloseEvent):
        self.isRunning = False
        return True

    def on_window_resize(self, windowResizeEvent : WindowResizeEvent):
        Renderer3D.set_viewport(windowResizeEvent.x, windowResizeEvent.y)
        Renderer3D.set_aspect_ratio(windowResizeEvent.x, windowResizeEvent.y)
        return True

    def on_key_pressed(self, keyPressedEvent : KeyPressedEvent):
        if keyPressedEvent.keyCode == KeyCode.ESC:
            self.isRunning = False
            return True

        return False

    def on_mouse_button_pressed(self, mouseButtonPressedEvent : MouseButtonPressedEvent):
        if mouseButtonPressedEvent.button == MouseCode.ButtonMiddle:
            self.isRunning = False
            return True

        return False

    def on_mouse_moved(self, mouseMovedEvent : MouseMovedEvent):
        return True

    def on_event(self, event):
        dispatcher = EventDispatcher(event)
        dispatcher.dispatch(self.on_window_close)
        dispatcher.dispatch(self.on_window_resize)
        dispatcher.dispatch(self.on_key_pressed)
        dispatcher.dispatch(self.on_mouse_moved)
        dispatcher.dispatch(self.on_mouse_button_pressed)

    def run(self):
        timeSinceLastUpdate = 0.0
        while self.isRunning:
            time = self.window.get_time()
            timestep = time - timeSinceLastUpdate
            timeSinceLastUpdate = time

            Renderer3D.clear()
            Renderer3D.drawTexturedCube((0.0, 0.0, 0.0), self.texture, 45.0)

            self.window.update()
        
        self.texture.cleanup()
        Renderer3D.cleanup() 
        self.window.cleanup()
