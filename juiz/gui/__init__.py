import gettext
import wx

from .Welcome import Welcome
from .Main import Main
from .Download import Download
from .. import buildpack

app = None

# emulation layer for ShowWindowModal if wxWidget is too old
if not getattr(wx.Dialog, 'ShowWindowModal', None):
	def ShowWindowModal(self):
		return self.ShowModal()

	wx.Dialog.ShowWindowModal = ShowWindowModal

def bootstrap():
	global app
	gettext.install("juiz")

	app = wx.PySimpleApp(0)
	wx.InitAllImageHandlers()

def run(project=None):
	global app
	if project:
		main = Main(project, None)
	else:
		main = Welcome(None, None)
	app.SetTopWindow(main)
	main.Show()

	check_buildpack()

	app.MainLoop()

def check_buildpack():
	if len(buildpack.list().keys()) == 0:
		if wx.MessageDialog(None, _('No buildpack are installed. Do you want to install basic buildpacks?'), _('No buildpack installed'), wx.YES_NO | wx.ICON_QUESTION).ShowModal() == wx.ID_YES:
			downloader = Download(buildpack.INITIAL_BUILDPACK.items(), None)
			downloader.run()
			downloader.ShowModal()

def error(msg):
	wx.MessageDialog(None, _(msg), _('Error'), wx.OK | wx.CENTRE | wx.ICON_ERROR).ShowModal()
	app.MainLoop()