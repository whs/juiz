import wx
import wx.lib.mixins.listctrl

class EditableListBox(wx.ListCtrl, wx.lib.mixins.listctrl.TextEditMixin):
	def __init__(self, *args, **kwargs):
		wx.ListCtrl.__init__(self, *args, **kwargs)
		wx.lib.mixins.listctrl.TextEditMixin.__init__(self)

		self.Unbind(wx.EVT_LEFT_DOWN, handler=self.OnLeftDown)

	def open(self, col, row):
		# copied from TextEditMixin's OnLeftDown

		if self.editor.IsShown():
		    self.CloseEditor()
		
		self.col_locs = [0]
		loc = 0
		for n in range(self.GetColumnCount()):
		    loc = loc + self.GetColumnWidth(n)
		    self.col_locs.append(loc)

		self.OpenEditor(col, row)