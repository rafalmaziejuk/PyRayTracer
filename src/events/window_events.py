from events.event import Event

class WindowCloseEvent(Event):
	def __init__(self):
		super().__init__()

class WindowResizeEvent(Event):
	def __init__(self, x, y):
		super().__init__()
		self.x = x
		self.y = y
