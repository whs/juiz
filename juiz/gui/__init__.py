import gettext
import wx

from .Welcome import Welcome
from .Main import Main

app = None

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
	app.MainLoop()

def error(msg):
	wx.MessageDialog(None, _(msg), _('Error'), wx.OK | wx.CENTRE | wx.ICON_ERROR).ShowModal()
	app.MainLoop()