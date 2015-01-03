import wx

from juiz.ui.EditMachine import EditMachine as Base
from juiz.roles import registry
from juiz.util import import_by_name

class EditMachine(Base):
	def __init__(self, parent, project, machine, *args, **kwargs):
		super(EditMachine, self).__init__(parent, *args, **kwargs)
		self.project = project
		self.machine = machine
		self.role_panel = {}

		self.name.SetValue(machine.name)
		self.list_box_1.SetCheckedStrings(machine.roles)
		self.SetTitle(_('Editing {}').format(machine.name))

		self.Bind(wx.EVT_BUTTON, self.on_save, id=wx.ID_SAVE)
		self.Bind(wx.EVT_BUTTON, self.on_cancel, id=wx.ID_CANCEL)
		# TODO: Add id
		self.Bind(wx.EVT_CHECKLISTBOX, self.on_list_changed)

		self.SetAffirmativeId(wx.ID_SAVE)
		self.SetEscapeId(wx.ID_CANCEL)

		self.load_roles()

	def on_cancel(self, event):
		self.Show(False)
		self.Close()

	def on_save(self, event=None):
		if self.machine.name != self.name.GetValue():
			self.project.config.remove_section('machine:{}'.format(self.machine.name))

		section = 'machine:{}'.format(self.name.GetValue())
		self.project.config.remove_section(section)
		self.project.config.add_section(section)

		for ind, name in enumerate(self.list_box_1.GetCheckedStrings()):
			self.project.config.set(section, 'role{}'.format(ind), name)

		for panel in self.role_panel.values():
			control = panel.GetPane().GetSizer().GetItem(0).GetWindow()
			control.save(self.project.config, section)

		self.GetParent().update_machine()
		self.Show(False)
		self.Close()

	def on_list_changed(self, event):
		checked = self.list_box_1.GetCheckedStrings()
		sizer = self.panel.GetSizer()

		for name in checked:
			if name not in self.role_panel:
				self.load_role_panel(name)
		for name in self.role_panel.keys():
			if name not in checked:
				sizer.Detach(self.role_panel[name])
				self.role_panel[name].Destroy()
				del self.role_panel[name]

	def load_roles(self):
		for role in self.machine.roles:
			self.load_role_panel(role)

	def load_role_panel(self, role):
		sizer = self.panel.GetSizer()
		role_cls = import_by_name(registry[role])
		if role_cls.machine_config_gui:
			self.role_panel[role] = wx.CollapsiblePane(self.panel, -1, role, style=wx.CP_NO_TLW_RESIZE)
			page = import_by_name(role_cls.machine_config_gui)(self.role_panel[role].GetPane(), self.project, self.machine)
			page.load_data(self.project.config, 'machine:{}'.format(self.machine.name))
			inner_sizer = wx.BoxSizer(wx.VERTICAL)
			inner_sizer.Add(page, 1, wx.EXPAND)
			self.role_panel[role].GetPane().SetSizer(inner_sizer)

			sizer.Add(self.role_panel[role], 0, wx.EXPAND)
		self.panel.Layout()
