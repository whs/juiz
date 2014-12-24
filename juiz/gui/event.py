import wx

class SimpleEvent(wx.PyEvent):
	event_type = wx.NewId()
	def __init__(self):
		wx.PyEvent.__init__(self)
		self.SetEventType(self.event_type)

class ValueEvent(SimpleEvent):
	value = None
	def __init__(self, value=None):
		super(ValueEvent, self).__init__()
		self.value = value