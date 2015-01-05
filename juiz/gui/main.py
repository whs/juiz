import os
import wx
import pipes

from wx.lib.agw import ultimatelistctrl as ulc

from ..project import *
from ..ui.Main import Main as MainGen
from .wizard.NewWizard import NewWizard
from .wizard.NewMachineWizard import NewMachineWizard
from .Deploy import Deploy
from .EditMachine import EditMachine
from .BuildpackList import BuildpackList
from .GetIPDialog import GetIPDialog
from . import util as gui_util

class Main(MainGen):
	ids = {
		'deploy': 1001,
		'bp_manage': 3001,
		'machine_list': 5000,
		'run_cmd': 4000
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
		self.Connect(self.ids['bp_manage'], -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.menu_buildpack)
		self.Connect(wx.ID_ABOUT, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.menu_about)
		self.Connect(self.ids['run_cmd'], -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.run_cmd)
		
		if self.project:
			self.Connect(wx.ID_SAVE, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.menu_save)
			self.Connect(wx.ID_REVERT_TO_SAVED, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.menu_revert)
			self.Connect(self.ids['deploy'], -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.menu_deploy)
			self.Bind(wx.EVT_BUTTON, self.add_machine, id=wx.ID_ADD)
			self.Bind(wx.EVT_BUTTON, self.edit_machine, id=wx.ID_EDIT)
			self.Bind(wx.EVT_BUTTON, self.remove_machine, id=wx.ID_REMOVE)
			self.Bind(wx.EVT_CLOSE, self.on_close)
			self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.edit_machine, id=self.ids['machine_list'])
			self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.menu_machine, id=self.ids['machine_list'])

			self.setup_project()
			self.refresh()

	def refresh(self):
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

	def menu_about(self, event):
		info = wx.AboutDialogInfo()
		info.SetName('Juiz')
		info.SetDescription(_('Desktop-Cloud Platform as a Service'))
		info.SetCopyright(_('(C) 2014 Juiz developers'))
		info.SetLicense(_('This application\'s development is sponsored by NECTEC'))
		info.AddDeveloper('Manatsawin Hanmongkolchai')

		wx.AboutBox(info)

	def menu_buildpack(self, event):
		BuildpackList(self).ShowModal()

	def menu_deploy(self, event):
		Deploy(self.project, self).ShowWindowModal()

	def menu_save(self, event):
		self.project.save_config(self.project.root)
		self.changed = False

	def menu_revert(self, event):
		if self.changed:
			if wx.MessageDialog(self, _('Revert any unsaved change to the latest saved version?'), _('Revert to saved'), wx.ICON_QUESTION | wx.YES_NO) == wx.YES:
				for section in self.project.config.sections():
					self.project.config.remove_section(section)

				self.project.load_config(self.project.root)
				self.changed = False
				self.refresh()

	def menu_machine(self, event):
		height = self.machine_list.GetItemRect(event.GetItem().GetId()).height
		header_height = self.machine_list.GetHeaderHeight().height
		point = event.GetPoint()
		point.y += height + header_height

		self._last_context = event.GetItem()

		menu = wx.Menu(event.GetItem().GetText())
		menu.Append(self.ids['run_cmd'], _('&Run command'))
		self.PopupMenu(menu, point)
		menu.Destroy()

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

	def edit_machine(self, event):
		machine = self.get_selected_machine()
		if not machine:
			wx.MessageDialog(self, _('No machine selected'), _('Edit machine'), wx.ICON_ASTERISK).ShowWindowModal()
			return

		EditMachine(self, self.project, machine).Show()

	def remove_machine(self, event):
		machine = self.get_selected_machine_name()
		if not machine:
			wx.MessageDialog(self, _('No machine selected'), _('Remove machine'), wx.ICON_ASTERISK).ShowWindowModal()
			return

		if wx.MessageBox(_('Remove {0}?').format(machine), _('Remove machine'), wx.ICON_QUESTION | wx.YES_NO) == wx.NO:
			return
		self.project.config.remove_section('machine:{}'.format(machine))
		self.update_machine()
		self.changed = True

	def get_selected_machine_name(self):
		selected = self.machine_list.GetFirstSelected()

		if selected == -1:
			return

		return self.machine_list.GetItemText(selected)

	def get_selected_machine(self):
		machine = self.get_selected_machine_name()
		if not machine:
			return

		return [x for x in self.project.list_machines() if x.name == machine][0]

	def run_cmd(self, evt):
		if not self._last_context:
			return

		machine = self.project.get_machine(self._last_context.GetText())
		ip_dialog = GetIPDialog(self.project, machine)
		if ip_dialog.ShowModal() == 0:
			wx.MessageDialog(self, _('IP of {} cannot be determined').format(machine.name), _('Cannot get IP'), wx.OK | wx.CENTER | wx.ICON_EXCLAMATION).ShowWindowModal()
			return

		dialog = wx.TextEntryDialog(self, _('Enter command. Web application is deployed at /app.'), _('Run command on {ip}'.format(ip=ip_dialog.ip)), 'bash')

		if dialog.ShowModal() == wx.ID_OK:
			cmd = 'ssh -i "{key}" -t "root@{ip}" "/var/juiz/remote/remote-login \'{cmd}\'"'.format(
				ip = ip_dialog.ip,
				key = os.path.expanduser(self.project.config.get('main', 'ssh_key')),
				cmd = pipes.quote(dialog.GetValue())
			)
			gui_util.run_terminal(cmd)
