import wx
from wx.lib.wordwrap import wordwrap
from wx.lib.stattext import GenStaticText as StaticText

# copied from wx.lib.agw.infobar
class AutoWrapStaticText(StaticText):
	def __init__(self, parent, label):
		StaticText.__init__(self, parent, -1, label, style=wx.ST_NO_AUTORESIZE)

		self.label = label

		self.Bind(wx.EVT_SIZE, self.OnSize)


	def OnSize(self, event):
		event.Skip()
		self.Wrap(event.GetSize().width)


	def Wrap(self, width):
		if width < 0:
			return
		
		self.Freeze()

		dc = wx.ClientDC(self)
		dc.SetFont(self.GetFont())
		text = wordwrap(self.label, width, dc)
		self.SetLabel(text, wrapped=True)

		self.Thaw()


	def SetLabel(self, label, wrapped=False):
		if not wrapped:
			self.label = label

		StaticText.SetLabel(self, label)
