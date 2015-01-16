import threading

import wx

from .event import SimpleEvent

class DestroyDialog(wx.ProgressDialog):
	PULSE_INTERVAL = 50
	
	def __init__(self, node, *args, **kwargs):
		self.node = node
		kwargs['style'] = wx.PD_AUTO_HIDE | wx.SYSTEM_MENU
		super(DestroyDialog, self).__init__(_('Destroy'), '', 100, *args, **kwargs)
		self.Pulse(_('Destroying {0}').format(self.node.name))
		self.Fit()

		self.timer = wx.Timer(self)
		self.timer.Start(self.PULSE_INTERVAL)

		self.Connect(-1, -1, CompletedEvent.event_type, self.on_complete)
		self.Bind(wx.EVT_TIMER, self.pulse, self.timer)
		DestroyThread(self.node, self).start()

	def pulse(self, evt):
		self.Pulse()

	def on_complete(self, evt):
		self.Update(100)
		self.timer.Stop()
		self.EndModal(True)

class DestroyThread(threading.Thread):
	def __init__(self, node, wnd):
		super(DestroyThread, self).__init__()
		self.node = node
		self.wnd = wnd

	def run(self):
		# TODO: Ask provider to destroy
		driver = self.node.driver
		driver.destroy_node(self.node)
		wx.PostEvent(self.wnd, CompletedEvent())

class CompletedEvent(SimpleEvent):
	event_type = wx.NewId()