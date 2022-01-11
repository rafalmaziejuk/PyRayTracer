from events.event import Event
from enum import IntEnum

class KeyCode(IntEnum):
	SPACE = 32,
	A = 65,
	D = 68,
	S = 83,
	W = 87,
	ESC = 256,
	RIGHT = 262,
	LEFT = 263,
	LEFT_SHIFT = 340,
	LEFT_CONTROL = 341

class KeyEvent(Event):
	def __init__(self, keyCode):
		super().__init__()
		self.keyCode = keyCode

class KeyPressedEvent(KeyEvent):
	def __init__(self, keyCode):
		super().__init__(keyCode)

class KeyReleasedEvent(KeyEvent):
	def __init__(self, keyCode):
		super().__init__(keyCode)
