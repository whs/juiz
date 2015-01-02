import wx

from juiz import roles

class RoleList(wx.CheckListBox):
	ignored = ['base']

	def __init__(self, *args, **kwargs):
		super(RoleList, self).__init__(*args, **kwargs)
		self.load_roles()

	def load_roles(self):
		items = [x for x in roles.registry.keys() if x not in self.ignored]
		self.InsertItems(items, 0)