import ConfigParser

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
		self.Bind(wx.EVT_BUTTON, self.on_env_add, id=wx.ID_ADD)
		self.Bind(wx.EVT_BUTTON, self.on_env_del, id=wx.ID_REMOVE)

		self.env.InsertColumn(0, _('Key'))
		self.env.InsertColumn(1, _('Value'))

		self.update_env()

	def cloud_config(self, evt):
		if CloudWizard(self.project, self).run():
			self.GetParent().changed = True

	def on_save(self, evt):
		try:
			self.project.config.remove_section('env')
		except ConfigParser.NoSectionError:
			pass

		self.project.config.add_section('env')

		for index in range(self.env.GetItemCount()):
			key = self.env.GetItem(index, 0).GetText()
			value = self.env.GetItem(index, 1).GetText()
			self.project.config.set('env', key, value)

		self.GetParent().changed = True
		self.Close()
		self.EndModal(True)

	def on_close(self, evt):
		self.EndModal(False)
		self.Destroy()

	def update_env(self):
		try:
			for ind, (k, v) in enumerate(self.project.get_env().items()):
				ind = self.env.InsertStringItem(ind, k)
				self.env.SetStringItem(ind, 1, v)
		except ConfigParser.NoSectionError:
			pass

	def on_env_add(self, event):
		row = self.env.GetItemCount()
		self.env.InsertStringItem(row, '')
		self.env.open(0, row)

	def on_env_del(self, event):
		selected = self.env.GetFirstSelected()

		if selected == -1:
			wx.MessageDialog(self, _('Nothing is selected'), _('Remove environment variable'), wx.ICON_ASTERISK).ShowWindowModal()
			return

		self.env.DeleteItem(selected)
