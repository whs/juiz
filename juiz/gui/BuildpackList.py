import wx

from wx.lib.agw import ultimatelistctrl as ulc

from juiz import buildpack
from juiz.ui.BuildpackList import BuildpackList as BPL
from .wizard.BuildpackAddWizard import BuildpackAddWizard
from .Download import Download

class BuildpackList(BPL):
	def __init__(self, *args, **kwargs):
		super(BuildpackList, self).__init__(*args, **kwargs)

		self.Bind(wx.EVT_BUTTON, self.on_close, id=wx.ID_CLOSE)
		self.Bind(wx.EVT_BUTTON, self.on_add, id=wx.ID_ADD)
		self.Bind(wx.EVT_BUTTON, self.on_del, id=wx.ID_REMOVE)

		self.update_list()

	def update_list(self):
		self.buildpack_list.ClearAll()
		self.buildpack_list.InsertColumn(0, _('Name'))
		self.buildpack_list.InsertColumn(1, _('Source'))

		self.buildpack_list.SetColumnWidth(0, 100)
		self.buildpack_list.SetColumnWidth(1, ulc.ULC_AUTOSIZE_FILL)

		for key, value in buildpack.list().items():
			self.buildpack_list.Append([key, value['source']])

	def on_close(self, event):
		self.EndModal(True)
		self.Destroy()

	def on_add(self, event):
		result = BuildpackAddWizard(self).run()
		if result:
			if result[0] in buildpack.list():
				wx.MessageDialog(self, _('{0} is already exists').format(result[0]), _('Buildpack already exists'), wx.OK | wx.CENTER | wx.ICON_INFORMATION).ShowWindowModal()
				return

			dl = Download([result], self)
			dl.run()
			dl.ShowModal()

			buildpack.load_cfg()
			self.update_list()

	def on_del(self, event):
		index = self.buildpack_list.GetFirstSelected()

		if index == -1:
			wx.MessageDialog(self, _('No buildpack is selected'), _('Empty selection'), wx.OK | wx.CENTER | wx.ICON_EXCLAMATION).ShowWindowModal()
			return

		name = self.buildpack_list.GetItem(index).GetText()

		if wx.MessageDialog(self, _('Remove buildpack {0}?').format(name), _('Remove buildpack'), wx.YES_NO | wx.CENTER | wx.ICON_QUESTION).ShowModal() == wx.ID_YES:
			buildpack.remove(name)
			buildpack.save_cfg()
			self.update_list()
