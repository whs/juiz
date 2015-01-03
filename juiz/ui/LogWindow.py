# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.6.8 on Sat Jan  3 15:27:26 2015
#

import wx
# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class LogWindow(wx.Dialog):
	def __init__(self, *args, **kwds):
		# begin wxGlade: LogWindow.__init__
		wx.Dialog.__init__(self, *args, **kwds)
		self.progressbar = wx.Gauge(self, wx.ID_ANY, 10)
		self.close_btn = wx.Button(self, wx.ID_CLOSE, "")
		self.log = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH)

		self.__set_properties()
		self.__do_layout()
		# end wxGlade

	def __set_properties(self):
		# begin wxGlade: LogWindow.__set_properties
		self.SetTitle(_("Progress"))
		self.SetSize((400, 500))
		self.close_btn.Enable(False)
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: LogWindow.__do_layout
		sizer_5 = wx.BoxSizer(wx.VERTICAL)
		sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_6.Add(self.progressbar, 1, wx.EXPAND | wx.ADJUST_MINSIZE, 0)
		sizer_6.Add(self.close_btn, 0, wx.LEFT | wx.ADJUST_MINSIZE, 5)
		sizer_5.Add(sizer_6, 0, wx.ALL | wx.EXPAND, 10)
		sizer_5.Add(self.log, 1, wx.EXPAND, 0)
		self.SetSizer(sizer_5)
		self.Layout()
		# end wxGlade

# end of class LogWindow
