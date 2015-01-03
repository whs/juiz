import wx
import wx.lib.mixins.listctrl

class EditableListBox(wx.ListCtrl, wx.lib.mixins.listctrl.TextEditMixin):
	def __init__(self, *args, **kwargs):
		wx.ListCtrl.__init__(self, *args, **kwargs)
		wx.lib.mixins.listctrl.TextEditMixin.__init__(self)