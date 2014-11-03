import os
import wx

from ..config import config
from ..ui.Main import Main as MainGen
from .NewWizard import NewWizard

class Main(MainGen):
	ids = {
		'file_new': 1000,
		'file_open': 1001,
		'exit': 3000,
		'proj_config': 2000,
		'bp_manage': 3001
	}
	project = None
	close_on_new = False

	def __init__(self, *args, **kwargs):
		super(Main, self).__init__(*args, **kwargs)
		self.Connect(self.ids['file_new'], -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.menu_new)
		self.Connect(self.ids['file_open'], -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.menu_open)
		self.Connect(self.ids['exit'], -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.menu_exit)

	def set_project(self, project):
		self.SetTitle('{0} - Juiz'.format(os.path.basename(project)))
		self.project = project

	def menu_new(self, event):
		path = NewWizard(self).run()
		if not path:
			return

		self.open_project(path)

		if self.close_on_new:
			self.Close()

	def menu_open(self, event):
		picker = wx.DirDialog(self, defaultPath=os.getcwd(), style=wx.DD_DIR_MUST_EXIST)
		if picker.ShowModal():
			path = picker.GetPath()
			if not os.path.isdir(os.path.join(path, config.get('main', 'project_folder'))):
				wx.MessageDialog(self, _('Project configuration folder not found.'), _('Error'), wx.OK | wx.CENTRE | wx.ICON_ERROR).ShowModal()
			else:
				self.open_project(path)
				if self.close_on_new:
					self.Close()

	def menu_exit(self, event):
		self.Close(True)

	@classmethod
	def open_project(cls, path):
		wnd = Main(None)
		wnd.set_project(path)
		wnd.Show()