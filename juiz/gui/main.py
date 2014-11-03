import gettext
import wx

from .Welcome import Welcome

def run():
	gettext.install("juiz")

	app = wx.PySimpleApp(0)
	wx.InitAllImageHandlers()
	main = Welcome(None, wx.ID_ANY)
	app.SetTopWindow(main)
	main.Show()
	app.MainLoop()