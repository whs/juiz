import threading

import wx

from .event import ValueEvent

class GetIPDialog(wx.ProgressDialog):
	ip = None

	def __init__(self, project, machine, *args, **kwargs):
		self.project = project
		self.machine = machine
		kwargs['style'] = wx.PD_AUTO_HIDE | wx.SYSTEM_MENU
		super(GetIPDialog, self).__init__(_('Getting IP'), '', 100, *args, **kwargs)
		self.Pulse(_('Getting IP of {0}').format(self.machine.name))

		self.Connect(-1, -1, CompletedEvent.event_type, self.on_complete)
		GetIPThread(self.project, self.machine, self).start()

	def on_complete(self, evt):
		self.ip = evt.value
		self.Update(100)
		self.EndModal(self.ip != None)
		self.Destroy()

class GetIPThread(threading.Thread):
	def __init__(self, project, machine, wnd):
		super(GetIPThread, self).__init__()
		self.project = project
		self.machine = machine
		self.wnd = wnd

	def run(self):
		try:
			self.ip = self.machine.get_ip(self.project)
		except Exception, e:
			print `e`
			self.ip = None
		wx.PostEvent(self.wnd, CompletedEvent(self.ip))

class CompletedEvent(ValueEvent):
	event_type = wx.NewId()