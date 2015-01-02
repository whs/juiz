import wx
import wx.wizard

from .page.BaseWizardPage import BaseWizardPage
from ..widget.RoleList import RoleList

class NewMachineWizard(wx.wizard.Wizard):
	def __init__(self, project, parent=None):
		self.project = project
		super(NewMachineWizard, self).__init__(parent, wx.ID_ANY, _('New machine'))
		self.SetPageSize((500, 400))

	def run(self):
		page1 = NewMachineWizardPage(self, self.project)
		if self.RunWizard(page1):
			page1.dump_config(self.project.config)
			return True
		return False

class NewMachineWizardPage(BaseWizardPage):
	def __init__(self, parent, project):
		self.project = project
		super(NewMachineWizardPage, self).__init__(parent)
		self.create_ui()

		parent.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, self.on_show)
		self.Bind(wx.EVT_TEXT, self.on_input_changed)
		self.Bind(wx.EVT_CHECKLISTBOX, self.on_input_changed)

	def create_ui(self):
		self.outer_sizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(self.outer_sizer)

		self.sizer = wx.FlexGridSizer(0, 2, 5, 15)
		self.sizer.AddGrowableCol(1)

		text = wx.StaticText(self, -1, _('Name'))
		self.sizer.Add(text, 1, wx.EXPAND)

		self.name = wx.TextCtrl(self, wx.NewId())
		self.name.SetFocus()
		self.sizer.Add(self.name, 1, wx.EXPAND)

		self.outer_sizer.Add(self.sizer, 0, wx.EXPAND)

		text = wx.StaticText(self, -1, _('Roles'))
		self.outer_sizer.Add(text, 0, wx.EXPAND)
		self.outer_sizer.AddSpacer(5)

		self.roles = RoleList(self)
		self.outer_sizer.Add(self.roles, 1, wx.EXPAND)

	def on_show(self, event):
		self.check_allow_forward()

	def on_input_changed(self, event):
		self.check_allow_forward()	

	def check_allow_forward(self):
		can_forward = self.name.GetValue() and len(self.roles.GetChecked()) > 0
		if self.name.GetValue() in [x.name for x in self.project.list_machines()]:
			can_forward = False
		self.enable_forward(can_forward)

	def dump_config(self, config):
		section = 'machine:{}'.format(self.name.GetValue())
		config.add_section(section)

		for ind, name in enumerate(self.roles.GetCheckedStrings()):
			config.set(section, 'role{}'.format(ind), name)
