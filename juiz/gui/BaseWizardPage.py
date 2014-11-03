import wx.wizard

class BaseWizardPage(wx.wizard.PyWizardPage):
	next = None
	prev = None

	def GetNext(self):
		return self.next

	def GetPrev(self):
		return self.prev

	def set_next(self, next):
		self.next = next
		next.prev = self

	def enable_forward(self, value):
		forward_btn = self.GetParent().FindWindowById(wx.ID_FORWARD)
		if value:
			forward_btn.Enable()
		else:
			forward_btn.Disable()

class WizardInputListPage(BaseWizardPage):
	fields = []
	_widgets = []
	help_text = ''
	hyperlink = {}
	_cache = {}

	def __init__(self, parent):
		super(WizardInputListPage, self).__init__(parent)
		outer_sizer = wx.BoxSizer(wx.VERTICAL)

		help_text = wx.StaticText(self, -1, self.help_text)
		help_text.Wrap(parent.GetSize().width - 140)
		outer_sizer.Add(help_text, 0, wx.EXPAND)

		for name, url in self.hyperlink.items():
			link = wx.HyperlinkCtrl(self, wx.ID_ANY, name, url)
			outer_sizer.Add(link, 0, 0)

		self.sizer = wx.GridSizer(0, 2, 5, 5)

		self.build_input_group()

		outer_sizer.Add(self.sizer, 0, wx.EXPAND)
		self.SetSizer(outer_sizer)
		
		parent.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, self.on_show)
		self.Bind(wx.EVT_TEXT, self.input_changed)

	def build_input_group(self):
		for i in self.fields:
			label = self.build_label(_(i))
			self.sizer.Add(label, 0, wx.ADJUST_MINSIZE | wx.ALIGN_CENTER_VERTICAL)

			input = self.build_input(i)
			self.sizer.Add(input, 1, wx.EXPAND)
			self._widgets.append((i, input))

	def build_label(self, text):
		return wx.StaticText(self, wx.ID_ANY, text)

	def build_input(self, name):
		attr = 'get_{0}'.format(name.lower().replace(' ', '_'))
		value = ''
		if hasattr(self, attr) or name in self._cache:
			ls = self._cache[name] if name in self._cache else getattr(self, attr)()
			if type(ls) in (dict, list):
				if type(ls) == dict:
					self._cache[name] = ls.items()
				return wx.Choice(self, wx.ID_ANY, choices=[x[1] for x in self._cache[name]])
			else:
				value = ls
				self._cache[name] = ls
		return wx.TextCtrl(self, wx.ID_ANY, value=value)

	def on_show(self, event):
		if event.GetPage() == self:
			return self.check_allow_forward()
		event.Skip()

	def input_changed(self, event):
		self.check_allow_forward()

	def check_allow_forward(self):
		self.enable_forward(self.is_all_fields_filled())

	def is_all_fields_filled(self):
		return True not in [x[1].IsEmpty() for x in self._widgets]

	def __del__(self):
		self.GetParent().Unbind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, handler=self.on_show)

	def get_values(self):
		out = []
		for k,v in self._widgets:
			value = None
			if isinstance(v, wx.Choice):
				value = v.GetSelection()
				attr = 'get_{0}'.format(k.lower().replace(' ', '_'))
				value = getattr(self, attr)().keys()[value]
			else:
				value = v.GetValue()
			out.append(value)
		return out