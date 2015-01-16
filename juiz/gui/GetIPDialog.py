import threading

import wx

from .event import ValueEvent

class GetIPDialog(wx.ProgressDialog):
	ip = None
	PULSE_INTERVAL = 50

	def __init__(self, project, machine, *args, **kwargs):
		self.project = project
		self.machine = machine
		kwargs['style'] = wx.PD_AUTO_HIDE | wx.SYSTEM_MENU
		super(GetIPDialog, self).__init__(_('Getting IP'), '', 100, *args, **kwargs)
		self.Pulse(_('Getting IP of {0}').format(self.machine.name))
		self.Fit()

		self.timer = wx.Timer(self)
		self.timer.Start(self.PULSE_INTERVAL)

		self.Connect(-1, -1, CompletedEvent.event_type, self.on_complete)
		self.Bind(wx.EVT_TIMER, self.pulse, self.timer)
		self.thread = GetIPThread(self.project, self.machine, self)
		self.thread.start()

	def pulse(self, evt):
		self.Pulse()

	def on_complete(self, evt):
		self.ip = evt.value
		self.node = self.thread.node
		self.Update(100)
		self.timer.Stop()
		self.EndModal(self.ip != None)

class GetIPThread(threading.Thread):
	def __init__(self, project, machine, wnd):
		super(GetIPThread, self).__init__()
		self.project = project
		self.machine = machine
		self.ip = None
		self.wnd = wnd

	def run(self):
		try:
			self.node = self.machine.get_node(self.project)
			if self.node:
				self.ip = self.node.public_ips[0]
		except Exception, e:
			print `e`
			self.node = None
			self.ip = None
		wx.PostEvent(self.wnd, CompletedEvent(self.ip))

class CompletedEvent(ValueEvent):
	event_type = wx.NewId()