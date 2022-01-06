from window import window
from events.event import EventDispatcher
from events.keyboard_events import KeyPressedEvent, KeyCode
from events.window_events import WindowCloseEvent

from graphics.renderer3d import Renderer3D
from graphics.meshes.cube import Cube
from graphics.meshes.sphere import Sphere
from graphics.light import Light
from graphics.camera import Camera

class Application():
    def __init__(self):
        self.isRunning = True
        self.camera = Camera(45.0, window.windowData.width / window.windowData.height, 0.1, 1000.0)
        window.set_event_callback(self.on_event)
        Renderer3D.init(window.windowData.width, 
                        window.windowData.height, 
                        (0.3, 0.3, 0.3),
                        self.camera)

    def on_event(self, event):
        dispatcher = EventDispatcher(event)
        dispatcher.dispatch(self.on_window_close)
        dispatcher.dispatch(self.on_key_pressed)

        self.camera.on_event(event)

    def on_update(self, timestep):
        self.camera.on_update(timestep)

    def run(self):
        lightSource = Light((0.0, 10.0, 0.0), (0.0, -1.0, 0.0), (1.0, 1.0, 1.0), 35.0)
        lightCube = Cube(lightSource.position, (1.0, 1.0, 1.0))
        lightCube.set_color((1.0, 1.0, 1.0))
        
        cube = Cube((-1.0, 0.5, -6.0), (1.0, 2.0, 1.0))
        cube.set_color((0.1, 0.2, 0.3))

        sphere = Sphere((1.0, 0.5, -4.0), 1.0, 64, 64)
        sphere.set_color((1.0, 0.0, 0.0))

        floor = Cube((0.0, -1.0, 0.0), (20.0, 1.0, 20.0))
        floor.set_color((0.5, 0.5, 0.5))

        timeSinceLastUpdate = 0.0
        while self.isRunning:
            time = window.get_time()
            timestep = time - timeSinceLastUpdate
            timeSinceLastUpdate = time

            self.on_update(timestep)

            Renderer3D.clear()
            Renderer3D.draw_colored(lightCube)
            Renderer3D.draw_illuminated(cube, lightSource)
            Renderer3D.draw_illuminated(sphere, lightSource)
            Renderer3D.draw_illuminated(floor, lightSource)

            window.update()
        
        lightCube.cleanup()
        cube.cleanup()
        sphere.cleanup()
        floor.cleanup()

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
