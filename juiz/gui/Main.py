import os
import wx

from ..config import config
from ..project import *
from ..ui.Main import Main as MainGen
from .NewWizard import NewWizard

from wx.lib.agw import ultimatelistctrl as ulc

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

	def __init__(self, project=None, *args, **kwargs):
		self.project = project
		super(Main, self).__init__(*args, **kwargs)
		self.Connect(self.ids['file_new'], -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.menu_new)
		self.Connect(self.ids['file_open'], -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.menu_open)
		self.Connect(self.ids['exit'], -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.menu_exit)
		
		if self.project:
			self.setup_project()
			self.update_machine()

	def menu_new(self, event):
		path = NewWizard(self).run()
		if not path:
			return

		self.open_project(Project(path))

		if self.close_on_new:
			self.Close()

	def menu_open(self, event):
		picker = wx.DirDialog(self, defaultPath=os.getcwd(), style=wx.DD_DIR_MUST_EXIST)
		if picker.ShowModal() == wx.ID_OK:
			path = picker.GetPath()
			try:
				project = Project(path)
			except NoProjectException:
				return wx.MessageDialog(self, _('Project configuration folder not found.'), _('Error'), wx.OK | wx.CENTRE | wx.ICON_ERROR).ShowModal()
			self.open_project(project)
			if self.close_on_new:
				self.Close()

	def menu_exit(self, event):
		self.Close(True)

	@classmethod
	def open_project(cls, project):
		wnd = Main(project, None)
		wnd.Show()

	def setup_project(self):
		self.SetTitle('{0} - Juiz'.format(self.project.name))
		
		columns = [_('Name'), _('Roles')]
		for index, name in enumerate(columns):
			self.machine_list.InsertColumn(index, name)

		self.machine_list.SetColumnWidth(0, 150)
		self.machine_list.SetColumnWidth(1, ulc.ULC_AUTOSIZE_FILL)

	def update_machine(self):
		self.machine_list.DeleteAllItems()

		for index, machine in enumerate(self.project.list_machines()):
			self.machine_list.InsertStringItem(index, machine.name)
			self.machine_list.SetStringItem(index, 1, ', '.join(machine.roles))