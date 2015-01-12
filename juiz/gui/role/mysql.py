import ConfigParser

import wx

from juiz.gui.widget.AutoWrapStaticText import AutoWrapStaticText
from . import BaseRoleConfig

class MySQLMachineConfig(BaseRoleConfig):
	def __init__(self, *args, **kwargs):
		super(MySQLMachineConfig, self).__init__(*args, **kwargs)

		self.layout()

	def layout(self):
		outer_sizer = wx.BoxSizer(wx.VERTICAL)
		sizer = wx.FlexGridSizer(0, 2, 5, 5)
		sizer.AddGrowableCol(1)

		text = wx.StaticText(self, -1, _('Root password'))
		sizer.Add(text, 1, wx.EXPAND)

		self.root = wx.TextCtrl(self, -1)
		sizer.Add(self.root, 1, wx.EXPAND)

		text = wx.StaticText(self, -1, _('App password'))
		sizer.Add(text, 1, wx.EXPAND)

		self.app = wx.TextCtrl(self, -1)
		sizer.Add(self.app, 1, wx.EXPAND)

		outer_sizer.Add(sizer, 0, wx.EXPAND)

		outer_sizer.AddSpacer(5)

		text = AutoWrapStaticText(self, _('Will save in plain text. Empty password will use hashed project ID as password.'))
		outer_sizer.Add(text, 0, wx.EXPAND)

		self.SetSizer(outer_sizer)
		self.Layout()

	def save(self, config, section):
		config.set(section, 'mysql_root', self.root.GetValue())
		config.set(section, 'mysql_app', self.app.GetValue())

	def load_data(self, config, section):
		try:
			self.root.SetValue(config.get(section, 'mysql_root'))
		except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
			pass

		try:
			self.app.SetValue(config.get(section, 'mysql_app'))
		except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
			pass