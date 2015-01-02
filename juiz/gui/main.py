import os
import wx

from ..project import *
from ..ui.Main import Main as MainGen
from .wizard.NewWizard import NewWizard
from .wizard.NewMachineWizard import NewMachineWizard
from .Deploy import Deploy

from wx.lib.agw import ultimatelistctrl as ulc

class Main(MainGen):
	ids = {
		'deploy': 1001,
		'bp_manage': 3001
	}
	project = None
	close_on_new = False
	_changed = False
	
	@property
	def changed(self):
	    return self._changed
	@changed.setter
	def changed(self, value):
		self._changed = value
		changed = '*' if value else ''
		self.SetTitle('{0}{1} - Juiz'.format(self.project.name, changed))

	def __init__(self, project=None, *args, **kwargs):
		self.project = project
		super(Main, self).__init__(*args, **kwargs)
		self.Center()

		self.Connect(wx.ID_NEW, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.menu_new)
		self.Connect(wx.ID_OPEN, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.menu_open)
		self.Connect(wx.ID_EXIT, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.menu_exit)
		self.Connect(self.ids['deploy'], -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.menu_deploy)
		self.Bind(wx.EVT_BUTTON, self.add_machine, id=wx.ID_ADD)
		self.Bind(wx.EVT_CLOSE, self.on_close)
		
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

	def menu_deploy(self, event):
		Deploy(self.project, self).Show()

	def on_close(self, event):
		if event.CanVeto() and self.changed:
			if wx.MessageBox(_('The configuration have not been saved. Continue closing?'), _('Unsaved change'), wx.ICON_QUESTION | wx.YES_NO) == wx.NO:
				return event.Veto()
		event.Skip()

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

	def add_machine(self, event):
		if NewMachineWizard(self.project, self).run():
			self.update_machine()
			self.changed = True
