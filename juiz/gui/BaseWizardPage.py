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
		result = self.get_input_type(name)
		name_code = name.lower().replace(' ', '_')

		if result == 'choice':
			self._cache[name] = getattr(self, 'get_{0}_choices'.format(name_code))().items()
			choice = wx.Choice(self, wx.ID_ANY, choices=[x[1] for x in self._cache[name]])
			default = self.get_default_value(name)
			if default:
				index = next(index for (index, d) in enumerate(self._cache[name]) if d[0] == default)
				choice.SetSelection(index)
			return choice
		elif result == 'file':
			return wx.FilePickerCtrl(self, wx.ID_ANY, path=self.get_default_value(name))
		else:
			return wx.TextCtrl(self, wx.ID_ANY, value=self.get_default_value(name))
	
	def get_default_value(self, name):
		name_code = name.lower().replace(' ', '_')
		if hasattr(self, 'get_{0}'.format(name_code)):
			return getattr(self, 'get_{0}'.format(name_code))()
		return ''

	def get_input_type(self, name):
		name_code = name.lower().replace(' ', '_')
		attr = 'get_{0}_type'.format(name_code)
		result = 'text'
		if hasattr(self, attr):
			result = getattr(self, attr)()
		return result

	def on_show(self, event):
		if event.GetPage() == self:
			return self.check_allow_forward()
		event.Skip()

	def input_changed(self, event):
		self.check_allow_forward()

	def check_allow_forward(self):
		self.enable_forward(self.is_all_fields_filled())

	def is_all_fields_filled(self):
		return False not in [bool(x) for x in self.get_values()]

	def __del__(self):
		self.GetParent().Unbind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, handler=self.on_show)

	def get_values(self):
		out = []
		for k,v in self._widgets:
			value = None
			if isinstance(v, wx.Choice):
				value = v.GetSelection()
				value = self._cache[k][value][0]
			elif isinstance(v, wx.PickerBase):
				value = v.GetPath()
			else:
				value = v.GetValue()
			out.append(value)
		return out