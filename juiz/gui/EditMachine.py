import wx

from juiz.ui.EditMachine import EditMachine as Base
from juiz.roles import registry
from juiz.util import import_by_name

class EditMachine(Base):
	ids = {
		'roles': 2000,
	}

	def __init__(self, parent, project, machine, *args, **kwargs):
		super(EditMachine, self).__init__(parent, *args, **kwargs)
		self.project = project
		self.machine = machine
		self.role_panel = {}

		self.name.SetValue(machine.name)
		self.roles.SetCheckedStrings(machine.roles)
		self.SetTitle(_('Editing {}').format(machine.name))

		self.env.InsertColumn(0, _('Key'))
		self.env.InsertColumn(1, _('Value'))

		self.update_env()

		self.Bind(wx.EVT_BUTTON, self.on_save, id=wx.ID_SAVE)
		self.Bind(wx.EVT_BUTTON, self.on_cancel, id=wx.ID_CANCEL)
		self.Bind(wx.EVT_BUTTON, self.on_env_add, id=wx.ID_ADD)
		self.Bind(wx.EVT_BUTTON, self.on_env_del, id=wx.ID_REMOVE)
		self.Bind(wx.EVT_CHECKLISTBOX, self.on_list_changed, id=self.ids['roles'])

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

		for ind, name in enumerate(self.roles.GetCheckedStrings()):
			self.project.config.set(section, 'role{}'.format(ind), name)

		for index in range(self.env.GetItemCount()):
			key = self.env.GetItem(index, 0).GetText()
			value = self.env.GetItem(index, 1).GetText()
			self.project.config.set(section, 'env_{}'.format(key), value)

		for panel in self.role_panel.values():
			control = panel.GetItem(0).GetWindow()
			control.save(self.project.config, section)

		self.GetParent().update_machine()
		self.GetParent().changed = True
		self.Show(False)
		self.Close()

	def on_list_changed(self, event):
		checked = self.roles.GetCheckedStrings()
		sizer = self.panel.GetSizer()

		for name in checked:
			if name not in self.role_panel:
				self.load_role_panel(name)
		for name in self.role_panel.keys():
			if name not in checked:
				self.role_panel[name].GetItem(0).GetWindow().Destroy()
				sizer.Detach(self.role_panel[name])
				self.role_panel[name].Destroy()
				del self.role_panel[name]

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

	def update_env(self):
		for ind, (k, v) in enumerate(self.machine.env.iteritems()):
			ind = self.env.InsertStringItem(ind, k)
			self.env.SetStringItem(ind, 1, v)

	def load_roles(self):
		for role in self.machine.roles:
			self.load_role_panel(role)

	def load_role_panel(self, role):
		sizer = self.panel.GetSizer()
		role_cls = import_by_name(registry[role])
		if role_cls.machine_config_gui:
			static_box = wx.StaticBox(self.panel, -1, role)
			self.role_panel[role] = box = wx.StaticBoxSizer(static_box, wx.VERTICAL)
			page = import_by_name(role_cls.machine_config_gui)(self.panel, self.project, self.machine)
			page.load_data(self.project.config, 'machine:{}'.format(self.machine.name))
			box.Add(page, 1, wx.EXPAND)

			sizer.Add(box, 0, wx.EXPAND)
		
		self.Layout()
