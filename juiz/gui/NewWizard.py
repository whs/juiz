import os
import ConfigParser

import wx
import wx.wizard

from . import CloudWizard
from .BaseWizardPage import BaseWizardPage
from ..config import config
from .. import util

class NewWizard(wx.wizard.Wizard):
	def __init__(self, parent=None):
		super(NewWizard, self).__init__(parent, wx.ID_ANY, _('New project'))

	def run(self):
		page1 = NewWizardSelectCodePathPage(self)
		page2 = CloudWizard.CloudPickProviderWizardPage(self)
		page1.set_next(page2)
		if self.RunWizard(page1):
			self.build_config(page1)
			return page1.get_path()

	def build_config(self, fp):
		page = fp
		cfg = ConfigParser.ConfigParser()

		try:
			os.mkdir(os.path.join(fp.get_path(), config.get('main', 'project_folder')))
		except OSError:
			return self.show_error(_('Project configuration folder already exists.\n\nDelete {0} in project folder to reinitialize').format(config.get('main', 'project_folder')))

		while page:
			page.dump_config(cfg)
			page = page.GetNext()

		config_file = os.path.join(fp.get_path(), config.get('main', 'project_folder'), 'config.cfg')
		cfg.write(open(config_file, 'w'))

		id_file = open(os.path.join(fp.get_path(), config.get('main', 'project_folder'), 'id'), 'w')
		id_file.write(util.random_id())

	def show_error(self, message):
		wx.MessageDialog(self.GetParent(), message, _('Error'), wx.OK | wx.CENTRE | wx.ICON_ERROR).ShowModal()

class NewWizardSelectCodePathPage(BaseWizardPage):
	def __init__(self, parent):
		super(NewWizardSelectCodePathPage, self).__init__(parent)
		outer_sizer = wx.BoxSizer(wx.VERTICAL)
		help_text = wx.StaticText(self, -1, _('Select the root of the codebase to be the project directory. This directory must be recognized by one of the installed buildpacks.'))
		help_text.Wrap(parent.GetSize().width - 140)
		outer_sizer.Add(help_text, 0, wx.EXPAND)

		label = wx.StaticText(self, -1, _('Code path: '))
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(label, 0, wx.ADJUST_MINSIZE | wx.ALIGN_CENTER_VERTICAL)

		self.input = wx.DirPickerCtrl(self, -1)
		# bugged on linux
		# self.input.SetPath(os.getcwd())
		sizer.Add(self.input, 1, wx.EXPAND)

		outer_sizer.Add(sizer, 0, wx.EXPAND)
		self.SetSizer(outer_sizer)
		
		parent.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, self.on_show)
		self.input.Bind(wx.EVT_DIRPICKER_CHANGED, self.dir_changed)

	def on_show(self, event):
		if event.GetPage() == self:
			return self.check_allow_forward()
		event.Skip()

	def check_allow_forward(self):
		self.enable_forward(self.input.GetPath())

	def dir_changed(self, event):
		if os.path.isdir(os.path.join(self.get_path(), config.get('main', 'project_folder'))):
			wx.MessageDialog(self.GetParent(), _('Project configuration folder already exists.\n\nDelete {0} in project folder to reinitialize').format(config.get('main', 'project_folder')), _('Error'), wx.OK | wx.CENTRE | wx.ICON_ERROR).ShowModal()
			self.input.SetPath('')
		self.check_allow_forward()

	def get_path(self):
		return self.input.GetPath()

	def dump_config(self, config):
		# write all default config here
		config.add_section('machine:main')
		config.set('machine:main', 'role1', 'web')
		config.set('machine:main', 'role2', 'mysql')
		config.set('machine:main', 'role3', 'memcache')