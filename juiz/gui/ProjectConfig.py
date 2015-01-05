import wx

from juiz.ui.ProjectConfig import ProjectConfig as PC

from .wizard.CloudWizard import CloudWizard

class ProjectConfig(PC):
	ids = {
		'cloud_config': 1000
	}

	def __init__(self, project, *args, **kwargs):
		self.project = project
		super(ProjectConfig, self).__init__(*args, **kwargs)

		self.Bind(wx.EVT_BUTTON, self.cloud_config, id=self.ids['cloud_config'])
		self.Bind(wx.EVT_BUTTON, self.on_close, id=wx.ID_CLOSE)
		self.Bind(wx.EVT_BUTTON, self.on_save, id=wx.ID_SAVE)

	def cloud_config(self, evt):
		if CloudWizard(self.project, self).run():
			self.GetParent().changed = True

	def on_save(self, evt):
		self.GetParent().changed = True
		self.Close()
		self.EndModal(True)

	def on_close(self, evt):
		self.Close()
		self.EndModal(False)