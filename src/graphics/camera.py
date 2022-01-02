from window import window
from graphics.renderer3d import Renderer3D
from events.event import EventDispatcher
from events.window_events import WindowResizeEvent
from events.mouse_events import MouseMovedEvent
from events.keyboard_events import KeyCode
from polled_input import Input
from glm import *

global window

class Camera():
    def __init__(self, fov, aspectRatio, nearClip, farClip):
        self.fov = fov
        self.aspectRatio = aspectRatio
        self.nearClip = nearClip
        self.farClip = farClip
        self.position = vec3(0.0, 0.0, 0.0)
        self.forward = vec3(0.0, 0.0, -1.0)
        self.right = vec3(0.0, 0.0, 0.0)
        self.up = vec3(0.0, 1.0, 0.0)
        self.yaw = -90.0
        self.pitch = 0.0
        self.movementSpeed = 2.5
        self.mouseSensitivity = 0.05
        self.lastMousePosition = Input.get_mouse_position(window.windowData.windowHandle)
        
        self.projectionMatrix = perspective(radians(fov), aspectRatio, nearClip, farClip)
        self.__update_camera_vectors()

    def __update_camera_vectors(self):
        self.forward = normalize(vec3(  cos(radians(self.yaw)) * cos(radians(self.pitch)),
                                        sin(radians(self.pitch)),
                                        sin(radians(self.yaw)) * cos(radians(self.pitch))))
        self.right = normalize(cross(self.forward, vec3(0.0, 1.0, 0.0)))
        self.up    = normalize(cross(self.right, self.forward))

    def get_view_matrix(self):
        return lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self):
        return self.projectionMatrix

    def update_projection_matrix(self):
        self.projectionMatrix = perspective(radians(self.fov), self.aspectRatio, self.nearClip, self.farClip)
        Renderer3D.update_projection_matrix(self.projectionMatrix)

    def update_viewport(self, width, height):
        self.aspectRatio = width / height
        Renderer3D.update_viewport(width, height)
        self.update_projection_matrix()

    def on_event(self, event):
        dispatcher = EventDispatcher(event)
        dispatcher.dispatch(self.on_window_resize)
        dispatcher.dispatch(self.on_mouse_moved)

    def on_update(self, timestep):
        velocity = self.movementSpeed * timestep
        
        if Input.is_key_pressed(window.windowData.windowHandle, KeyCode.W):
            self.position += self.forward * velocity

        if Input.is_key_pressed(window.windowData.windowHandle, KeyCode.A):
            self.position -= self.right * velocity

        if Input.is_key_pressed(window.windowData.windowHandle, KeyCode.S):
            self.position -= self.forward * velocity

        if Input.is_key_pressed(window.windowData.windowHandle, KeyCode.D):
            self.position += self.right * velocity

        if Input.is_key_pressed(window.windowData.windowHandle, KeyCode.SPACE):
            self.position.y += velocity

        if Input.is_key_pressed(window.windowData.windowHandle, KeyCode.LEFT_CONTROL):
            self.position.y -= velocity

        if Input.is_key_pressed(window.windowData.windowHandle, KeyCode.LEFT_SHIFT):
            self.movementSpeed = 10.0
        else:
            self.movementSpeed = 2.5
        
    def on_window_resize(self, windowResizeEvent : WindowResizeEvent):
        if windowResizeEvent.x == 0 or windowResizeEvent.y == 0:
            return False

        self.update_viewport(windowResizeEvent.x, windowResizeEvent.y)
        return True
            
    def on_mouse_moved(self, mouseMovedEvent : MouseMovedEvent):
        deltaX = (mouseMovedEvent.x - self.lastMousePosition.x) * self.mouseSensitivity
        deltaY = (self.lastMousePosition.y - mouseMovedEvent.y) * self.mouseSensitivity
        self.lastMousePosition = vec2(mouseMovedEvent.x, mouseMovedEvent.y)

        self.yaw += deltaX
        self.pitch += deltaY

        if self.pitch > 89.0:
            self.pitch = 89.0
        if self.pitch < -89.0:
            self.pitch = -89.0

        self.__update_camera_vectors()
        return True
