import ConfigParser
from collections import OrderedDict

import wx.wizard

from juiz.gui.widget.AutoWrapStaticText import AutoWrapStaticText

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

	def get_project(self):
		parent = self.GetParent()
		return getattr(parent, 'project', None)

class WizardInputListPage(BaseWizardPage):
	fields = []
	help_text = ''
	hyperlink = {}
	nullable_field = []
	config_section = ''

	def __init__(self, parent):
		super(WizardInputListPage, self).__init__(parent)
		self._widgets = OrderedDict()
		self._cache = {}

		outer_sizer = wx.BoxSizer(wx.VERTICAL)

		if self.help_text:
			help_text = AutoWrapStaticText(self, self.help_text)
			help_text.Wrap(parent.GetPageSize().width)
			outer_sizer.Add(help_text, 0, wx.EXPAND)
			outer_sizer.AddSpacer(4)

		for name, url in self.hyperlink.items():
			link = wx.HyperlinkCtrl(self, wx.ID_ANY, name, url)
			outer_sizer.Add(link, 0, 0)
			outer_sizer.AddSpacer(2)

		outer_sizer.AddSpacer(10)

		self.sizer = wx.FlexGridSizer(0, 2, 5, 15)
		self.sizer.AddGrowableCol(1)

		self.build_input_group()

		outer_sizer.Add(self.sizer, 1, wx.EXPAND)
		self.SetSizer(outer_sizer)
		
		parent.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, self.on_show)
		self.Bind(wx.EVT_TEXT, self.input_changed)
		self.Bind(wx.EVT_FILEPICKER_CHANGED, self.input_changed)
		self.Bind(wx.EVT_CHOICE, self.input_changed)

	def build_input_group(self):
		for i in self.fields:
			label = self.build_label(_(i))
			self.sizer.Add(label, 0, wx.ADJUST_MINSIZE | wx.ALIGN_CENTER_VERTICAL)

			input = self.build_input(i)
			self.sizer.Add(input, 1, wx.EXPAND)
			self._widgets[i] = input

	def build_label(self, text):
		return wx.StaticText(self, wx.ID_ANY, text)

	def format_field_name(self, name):
		return name.lower().replace(' ', '_')

	def build_input(self, name):
		result = self.get_input_type(name)
		name_code = self.format_field_name(name)

		if result == 'choice':
			self._cache[name_code] = getattr(self, 'get_{0}_choices'.format(name_code))().items()
			choice = wx.Choice(self, wx.NewId(), choices=[x[1] for x in self._cache[name_code]])
			default = self.get_default_value(name)
			if default:
				try:
					index = next(index for (index, d) in enumerate(self._cache[name_code]) if d[0] == default)
					choice.SetSelection(index)
				except StopIteration:
					pass
			return choice
		elif result == 'file':
			return wx.FilePickerCtrl(self, wx.NewId(), path=self.get_default_value(name))
		else:
			return wx.TextCtrl(self, wx.NewId(), value=self.get_default_value(name))
	
	def get_default_value(self, name):
		name_code = self.format_field_name(name)

		try:
			return self.get_project().config.get(self.config_section, name_code)
		except (AttributeError, ConfigParser.NoOptionError, ConfigParser.NoSectionError):
			pass

		if hasattr(self, 'get_{0}'.format(name_code)):
			return getattr(self, 'get_{0}'.format(name_code))()
		return ''

	def get_input_type(self, name):
		name_code = self.format_field_name(name)
		attr = 'get_{0}_type'.format(name_code)
		result = 'text'
		if hasattr(self, attr):
			result = getattr(self, attr)()
		return result

	def get_widget(self, name):
		try:
			return self._widgets[name]
		except KeyError:
			return None

	def on_show(self, event):
		if event.GetPage() == self:
			return self.check_allow_forward()
		event.Skip()

	def input_changed(self, event):
		self.check_allow_forward()

	def check_allow_forward(self):
		self.enable_forward(self.is_all_fields_filled())

	def is_all_fields_filled(self):
		return all([bool(v) for k, v in self.get_values_dict(False).iteritems() if k not in self.nullable_field])

	def __del__(self):
		self.GetParent().Unbind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, handler=self.on_show)

	def get_values_dict(self, format_name=True):
		out = OrderedDict()
		for k,v in self._widgets.iteritems():
			if format_name:
				k = self.format_field_name(k)
			value = self.get_widget_value(k, v)
			out[k] = value
		return out

	def get_widget_value(self, field, widget):
		if isinstance(widget, wx.Choice):
			value = widget.GetSelection()
			return self._cache[self.format_field_name(field)][value][0]
		elif isinstance(widget, wx.PickerBase):
			return widget.GetPath()
		else:
			return widget.GetValue()

	def get_settings(self):
		return self.get_values_dict()

	def dump_config(self, config):
		try:
			config.add_section(self.config_section)
		except ConfigParser.DuplicateSectionError:
			pass
		
		for k, v in self.get_settings().iteritems():
			config.set(self.config_section, k, v)
