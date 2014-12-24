import wx

from .Main import Main

class Welcome(Main):
	close_on_new = True

	def _Main__do_layout(self):
		# cause lingering frame in osx if not destroyed
		self.notebook_1.Destroy()
		# remove the project menu
		menubar = self.GetMenuBar()
		menubar.EnableTop(menubar.FindMenu(_('&Project')), False)
		self.frame_1_toolbar.EnableTool(wx.ID_PROPERTIES, False)
		self.frame_1_toolbar.EnableTool(self.ids['deploy'], False)