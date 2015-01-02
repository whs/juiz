# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.6.8 on Fri Jan  2 10:08:33 2015
#

import wx
# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class EditMachine(wx.Dialog):
	def __init__(self, *args, **kwds):
		# begin wxGlade: EditMachine.__init__
		kwds["style"] = wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)
		self.panel_2 = wx.Panel(self, wx.ID_ANY)
		self.label_1 = wx.StaticText(self.panel_2, wx.ID_ANY, _("Name"))
		self.name = wx.TextCtrl(self.panel_2, wx.ID_ANY, "")
		self.label_2 = wx.StaticText(self.panel_2, wx.ID_ANY, _("Roles"))
		self.list_box_1 = wxCheckListBox(self.panel_2, wx.ID_ANY, choices=[], style=wx.LB_MULTIPLE | wx.LB_ALWAYS_SB)
		self.save = wx.Button(self, wx.ID_SAVE, "")
		self.cancel = wx.Button(self, wx.ID_CANCEL, "")

		self.__set_properties()
		self.__do_layout()
		# end wxGlade

	def __set_properties(self):
		# begin wxGlade: EditMachine.__set_properties
		self.SetTitle(_("dialog_2"))
		self.SetSize((600, 400))
		self.name.SetMinSize((0, 28))
		self.name.SetFocus()
		self.list_box_1.SetMinSize((0,120))
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: EditMachine.__do_layout
		sizer_7 = wx.BoxSizer(wx.VERTICAL)
		sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_9 = wx.BoxSizer(wx.VERTICAL)
		sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_10.Add(self.label_1, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.ADJUST_MINSIZE, 10)
		sizer_10.Add(self.name, 1, wx.EXPAND | wx.ADJUST_MINSIZE, 0)
		sizer_9.Add(sizer_10, 0, wx.BOTTOM | wx.EXPAND, 10)
		sizer_9.Add(self.label_2, 0, wx.BOTTOM | wx.ADJUST_MINSIZE, 5)
		sizer_9.Add(self.list_box_1, 0, wx.EXPAND | wx.ADJUST_MINSIZE, 0)
		self.panel_2.SetSizer(sizer_9)
		sizer_7.Add(self.panel_2, 1, wx.ALL | wx.EXPAND, 5)
		sizer_8.Add(self.save, 0, wx.ADJUST_MINSIZE, 0)
		sizer_8.Add(self.cancel, 0, wx.ADJUST_MINSIZE, 0)
		sizer_7.Add(sizer_8, 0, wx.ALL | wx.ALIGN_BOTTOM | wx.ALIGN_CENTER_HORIZONTAL | wx.ADJUST_MINSIZE, 10)
		self.SetSizer(sizer_7)
		self.Layout()
		self.Centre()
		# end wxGlade

# end of class EditMachine