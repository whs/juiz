import wx
import wx.wizard

from juiz.gui.widget.AutoWrapStaticText import AutoWrapStaticText
from .page.BaseWizardPage import BaseWizardPage

class BuildpackAddWizard(wx.wizard.Wizard):
	def __init__(self, parent=None):
		super(BuildpackAddWizard, self).__init__(parent, wx.ID_ANY, _('Add buildpack wizard'))
		self.SetPageSize((400, 300))

	def run(self):
		page1 = BuildpackAddPage(self)
		if self.RunWizard(page1):
			return (page1.name.GetValue(), page1.url.GetValue())
		return False

class BuildpackAddPage(BaseWizardPage):
	def __init__(self, parent):
		super(BuildpackAddPage, self).__init__(parent)
		self.create_ui()

		parent.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, self.on_show)
		self.Bind(wx.EVT_TEXT, self.on_input_changed)

	def create_ui(self):
		self.outer_sizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(self.outer_sizer)

		text = AutoWrapStaticText(self, _('Buildpack is a set of scripts to detect, install and deploy web applications. Any applications installed by Juiz must be supported by a buildpack. Juiz\'s buildpack is partially compatible with Heroku\'s but might require some modification to supports CentOS 7.\n\nThe buildpack URL must points to a Git repository which is clonable both locally and on the deployed machine without authentication.'))
		self.outer_sizer.Add(text, 0, wx.EXPAND)
		self.outer_sizer.AddSpacer(10)

		link = wx.HyperlinkCtrl(self, wx.ID_ANY, _('Deis buildpack list'), _('http://docs.deis.io/en/latest/using_deis/using-buildpacks/#included-buildpacks'))
		self.outer_sizer.Add(link, 0)
		self.outer_sizer.AddSpacer(10)


		self.sizer = wx.FlexGridSizer(0, 2, 5, 15)
		self.sizer.AddGrowableCol(1)

		text = wx.StaticText(self, -1, _('Name'))
		self.sizer.Add(text, 1, wx.EXPAND)

		self.name = wx.TextCtrl(self, wx.NewId())
		self.name.SetFocus()
		self.sizer.Add(self.name, 1, wx.EXPAND)

		text = wx.StaticText(self, -1, _('URL'))
		self.sizer.Add(text, 1, wx.EXPAND)

		self.url = wx.TextCtrl(self, wx.NewId())
		self.sizer.Add(self.url, 1, wx.EXPAND)

		self.outer_sizer.Add(self.sizer, 0, wx.EXPAND)

	def on_show(self, event):
		self.check_allow_forward()

	def on_input_changed(self, event):
		self.check_allow_forward()	

	def check_allow_forward(self):
		can_forward = self.name.GetValue() and self.url.GetValue()
		self.enable_forward(can_forward)
