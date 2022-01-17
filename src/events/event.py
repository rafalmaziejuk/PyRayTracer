from inspect import formatargspec, getfullargspec
from re import search

class Event():
	def __init__(self):
		self.isHandled = False

class EventDispatcher():
	def __init__(self, event):
		self.eventType = search("events.(.*?)'", str(type(event))).group(1)
		self.event = event

	def dispatch(self, callback):
		argsFormat = formatargspec(*getfullargspec(callback))
		callbackEventType = search("events.(.*?)\)", argsFormat).group(1)
		
		if self.eventType == callbackEventType:
			self.event.isHandled |= callback(self.event)
			return True

		return False
