from events.event import Event
from enum import IntEnum

class MouseCode(IntEnum):
	ButtonLeft = 0,
	ButtonRight = 1,
	ButtonMiddle = 2

class MouseMovedEvent(Event):
	def __init__(self, x, y):
		super().__init__()
		self.x = x
		self.y = y

class MouseScrollEvent(Event):
	def __init__(self, x, y):
		super().__init__()
		self.x = x
		self.y = y

class MouseButtonEvent(Event):
	def __init__(self, button):
		super().__init__()
		self.button = button


class MouseButtonPressedEvent(MouseButtonEvent):
	def __init__(self, button):
		super().__init__(button)

class MouseButtonReleasedEvent(MouseButtonEvent):
	def __init__(self, button):
		super().__init__(button)
