import wx

class BaseRoleConfig(wx.Window):
	def __init__(self, parent, project, machine, *args, **kwargs):
		super(BaseRoleConfig, self).__init__(parent, *args, **kwargs)
		self.project = project
		self.machine = machine

	def save(self, config, section):
		pass

	def load_data(self, config, section):
		pass