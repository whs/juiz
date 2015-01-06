# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.6.8 on Tue Jan  6 12:11:45 2015
#

import wx
# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
from wx.lib.agw.ultimatelistctrl import UltimateListCtrl
# end wxGlade


class Main(wx.Frame):
	def __init__(self, *args, **kwds):
		# begin wxGlade: Main.__init__
		kwds["style"] = wx.DEFAULT_FRAME_STYLE
		wx.Frame.__init__(self, *args, **kwds)
		
		# Menu Bar
		self.frame_1_menubar = wx.MenuBar()
		wxglade_tmp_menu = wx.Menu()
		wxglade_tmp_menu.Append(wx.ID_NEW, _("&New project\tCtrl+N"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(wx.ID_OPEN, _("&Open project\tCtrl+O"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(wx.ID_SAVE, _("Save\tCtrl+S"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(wx.ID_REVERT_TO_SAVED, _("Revert to Saved"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.AppendSeparator()
		wxglade_tmp_menu.Append(wx.ID_EXIT, _("&Quit\tCtrl+W"), "", wx.ITEM_NORMAL)
		self.frame_1_menubar.Append(wxglade_tmp_menu, _("&File"))
		wxglade_tmp_menu = wx.Menu()
		wxglade_tmp_menu.Append(wx.ID_COPY, _("&Copy\tCtrl+C"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(wx.ID_CUT, _("Cu&t\tCtrl+X"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(wx.ID_PASTE, _("&Paste\tCtrl+V"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.AppendSeparator()
		wxglade_tmp_menu.Append(3001, _("&Buildpack management"), "", wx.ITEM_NORMAL)
		self.frame_1_menubar.Append(wxglade_tmp_menu, _("&Edit"))
		wxglade_tmp_menu = wx.Menu()
		wxglade_tmp_menu.Append(wx.ID_PROPERTIES, _("&Configuration"), "", wx.ITEM_NORMAL)
		self.frame_1_menubar.Append(wxglade_tmp_menu, _("&Project"))
		wxglade_tmp_menu = wx.Menu()
		wxglade_tmp_menu.Append(wx.ID_ABOUT, _("&About"), "", wx.ITEM_NORMAL)
		self.frame_1_menubar.Append(wxglade_tmp_menu, _("&Help"))
		self.SetMenuBar(self.frame_1_menubar)
		# Menu Bar end
		
		# Tool Bar
		self.frame_1_toolbar = wx.ToolBar(self, -1, style=wx.TB_HORIZONTAL | wx.TB_TEXT | wx.TB_NOICONS | wx.TB_HORZ_LAYOUT | wx.TB_HORZ_TEXT)
		self.SetToolBar(self.frame_1_toolbar)
		self.frame_1_toolbar.AddLabelTool(wx.ID_NEW, _("New"), wx.NullBitmap, wx.NullBitmap, wx.ITEM_NORMAL, "", "")
		self.frame_1_toolbar.AddLabelTool(wx.ID_OPEN, _("Open"), wx.NullBitmap, wx.NullBitmap, wx.ITEM_NORMAL, "", "")
		self.frame_1_toolbar.AddLabelTool(wx.ID_PROPERTIES, _("Configuration"), wx.NullBitmap, wx.NullBitmap, wx.ITEM_NORMAL, "", "")
		self.frame_1_toolbar.AddLabelTool(1001, _("Deploy"), wx.NullBitmap, wx.NullBitmap, wx.ITEM_NORMAL, "", "")
		# Tool Bar end
		self.notebook_1 = wx.Notebook(self, wx.ID_ANY, style=0)
		self.notebook_1_pane_1 = wx.Panel(self.notebook_1, wx.ID_ANY)
		self.machine_list = UltimateListCtrl(self.notebook_1_pane_1, 5000, agwStyle=wx.LC_REPORT|wx.LC_VRULES|wx.LC_HRULES)
		self.machine_add = wx.Button(self.notebook_1_pane_1, wx.ID_ADD, "")
		self.machine_edit = wx.Button(self.notebook_1_pane_1, wx.ID_EDIT, _("&Edit"))
		self.machine_remove = wx.Button(self.notebook_1_pane_1, wx.ID_REMOVE, "")
		self.panel_1 = wx.Panel(self.notebook_1, wx.ID_ANY)

		self.__set_properties()
		self.__do_layout()
		# end wxGlade

	def __set_properties(self):
		# begin wxGlade: Main.__set_properties
		self.SetTitle(_("Juiz"))
		self.SetSize((500, 600))
		self.frame_1_toolbar.Realize()
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: Main.__do_layout
		sizer_1 = wx.BoxSizer(wx.VERTICAL)
		sizer_4 = wx.BoxSizer(wx.VERTICAL)
		sizer_2 = wx.BoxSizer(wx.VERTICAL)
		sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_2.Add(self.machine_list, 1, wx.EXPAND, 0)
		sizer_3.Add(self.machine_add, 0, wx.RIGHT | wx.ADJUST_MINSIZE, 10)
		sizer_3.Add(self.machine_edit, 0, wx.RIGHT | wx.ADJUST_MINSIZE, 10)
		sizer_3.Add(self.machine_remove, 0, wx.ADJUST_MINSIZE, 0)
		sizer_2.Add(sizer_3, 0, wx.ALL | wx.ALIGN_BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, 10)
		self.notebook_1_pane_1.SetSizer(sizer_2)
		self.panel_1.SetSizer(sizer_4)
		self.notebook_1.AddPage(self.notebook_1_pane_1, _("Machines"))
		self.notebook_1.AddPage(self.panel_1, _("Addons"))
		sizer_1.Add(self.notebook_1, 1, wx.EXPAND, 0)
		self.SetSizer(sizer_1)
		self.Layout()
		self.Centre()
		# end wxGlade

# end of class Main
