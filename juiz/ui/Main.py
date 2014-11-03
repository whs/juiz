# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.6.8 on Wed Oct 29 08:40:03 2014
#

import wx
# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class Main(wx.Frame):
	def __init__(self, *args, **kwds):
		# begin wxGlade: Main.__init__
		kwds["style"] = wx.DEFAULT_FRAME_STYLE
		wx.Frame.__init__(self, *args, **kwds)
		
		# Menu Bar
		self.frame_1_menubar = wx.MenuBar()
		wxglade_tmp_menu = wx.Menu()
		wxglade_tmp_menu.Append(1000, _("&New project"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(1001, _("&Open project"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.AppendSeparator()
		wxglade_tmp_menu.Append(3000, _("E&xit"), "", wx.ITEM_NORMAL)
		self.frame_1_menubar.Append(wxglade_tmp_menu, _("&File"))
		wxglade_tmp_menu = wx.Menu()
		wxglade_tmp_menu.Append(3001, _("&Buildpack management"), "", wx.ITEM_NORMAL)
		self.frame_1_menubar.Append(wxglade_tmp_menu, _("&Edit"))
		wxglade_tmp_menu = wx.Menu()
		wxglade_tmp_menu.Append(2000, _("&Configuration"), "", wx.ITEM_NORMAL)
		self.frame_1_menubar.Append(wxglade_tmp_menu, _("&Project"))
		self.SetMenuBar(self.frame_1_menubar)
		# Menu Bar end
		
		# Tool Bar
		self.frame_1_toolbar = wx.ToolBar(self, -1)
		self.SetToolBar(self.frame_1_toolbar)
		self.frame_1_toolbar.AddLabelTool(1000, _("New"), wx.NullBitmap, wx.NullBitmap, wx.ITEM_NORMAL, "", "")
		self.frame_1_toolbar.AddLabelTool(1001, _("Open"), wx.NullBitmap, wx.NullBitmap, wx.ITEM_NORMAL, "", "")
		self.frame_1_toolbar.AddLabelTool(2000, _("Configuration"), wx.NullBitmap, wx.NullBitmap, wx.ITEM_NORMAL, "", "")
		# Tool Bar end
		self.notebook_1 = wx.Notebook(self, wx.ID_ANY, style=0)
		self.notebook_1_pane_1 = wx.Panel(self.notebook_1, wx.ID_ANY)
		self.list_ctrl_1 = wx.ListCtrl(self.notebook_1_pane_1, wx.ID_ANY, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
		self.machine_add = wx.Button(self.notebook_1_pane_1, wx.ID_ANY, _("Add"))
		self.machine_edit = wx.Button(self.notebook_1_pane_1, wx.ID_ANY, _("Edit"))
		self.machine_remove = wx.Button(self.notebook_1_pane_1, wx.ID_ANY, _("Remove"))
		self.notebook_1_pane_2 = wx.Panel(self.notebook_1, wx.ID_ANY)

		self.__set_properties()
		self.__do_layout()
		# end wxGlade

	def __set_properties(self):
		# begin wxGlade: Main.__set_properties
		self.SetTitle(_("Juiz"))
		self.SetSize((500, 517))
		self.frame_1_toolbar.Realize()
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: Main.__do_layout
		sizer_1 = wx.BoxSizer(wx.VERTICAL)
		sizer_2 = wx.BoxSizer(wx.VERTICAL)
		sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_2.Add(self.list_ctrl_1, 1, wx.EXPAND, 0)
		sizer_3.Add(self.machine_add, 0, wx.ADJUST_MINSIZE, 0)
		sizer_3.Add(self.machine_edit, 0, wx.ADJUST_MINSIZE, 0)
		sizer_3.Add(self.machine_remove, 0, wx.ADJUST_MINSIZE, 0)
		sizer_2.Add(sizer_3, 0, wx.ALIGN_BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, 0)
		self.notebook_1_pane_1.SetSizer(sizer_2)
		self.notebook_1.AddPage(self.notebook_1_pane_1, _("Machines"))
		self.notebook_1.AddPage(self.notebook_1_pane_2, _("Addons"))
		sizer_1.Add(self.notebook_1, 1, wx.EXPAND, 0)
		self.SetSizer(sizer_1)
		self.Layout()
		self.Centre()
		# end wxGlade

# end of class Main