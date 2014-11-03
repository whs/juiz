import wx

from .Main import Main

class Welcome(Main):
	close_on_new = True

	def _Main__do_layout(self):
		# remove the project menu
		menubar = self.GetMenuBar()
		menubar.Remove(menubar.FindMenu(_('&Project')))