#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.6.8 on Thu Nov 13 09:58:04 2014
#

# This is an automatically generated file.
# Manual changes will be overwritten without warning!

import wx
import gettext
from Main import Main

if __name__ == "__main__":
	gettext.install("app") # replace with the appropriate catalog name

	app = wx.PySimpleApp(0)
	wx.InitAllImageHandlers()
	main = Main(None, wx.ID_ANY, "")
	app.SetTopWindow(main)
	main.Show()
	app.MainLoop()