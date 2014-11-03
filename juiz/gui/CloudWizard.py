import importlib

import wx

from .BaseWizardPage import BaseWizardPage
from libcloud.compute.types import Provider

class CloudPickProviderWizardPage(BaseWizardPage):
	providers = {
		'Amazon Elastic Compute Cloud (EC2)': {
			'id': 100001,
			'next': 'juiz.gui.aws.AWSCloudConfigWizardPage',
			'provider': Provider.EC2
		},
		'DigitalOcean': {
			'id': 100002,
			'next': 'juiz.gui.digitalocean.DOCloudConfigWizardPage',
			'provider': Provider.DIGITAL_OCEAN
		},
		'Apache CloudStack': {
			'id': 100003,
			'provider': Provider.CLOUDSTACK
		},
	}

	def __init__(self, parent):
		super(CloudPickProviderWizardPage, self).__init__(parent)
		outer_sizer = wx.BoxSizer(wx.VERTICAL)
		help_text = wx.StaticText(self, -1, _('Select cloud provider to configure:'))
		help_text.Wrap(parent.GetSize().width - 140)
		outer_sizer.Add(help_text, 0, wx.EXPAND)
		outer_sizer.AddSpacer(10)

		self.radio = []

		for k,v in self.providers.items():
			self.create_radio(_(k), v['id'])

		for radio in self.radio:
			outer_sizer.Add(radio, 0, wx.EXPAND)
		
		self.SetSizer(outer_sizer)
		self.pick_radio(self.providers.values()[0])

		parent.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, self.on_show)
		self.Bind(wx.EVT_RADIOBUTTON, self.radio_change)

	def on_show(self, event):
		if event.GetPage() == self:
			self.enable_forward(True)
		event.Skip()

	def create_radio(self, name, id=wx.ID_ANY):
		radio = wx.RadioButton(self, id, name)
		self.radio.append(radio)

	def radio_change(self, event):
		id = event.GetId()
		data = self.get_data_by_id(id)

		self.pick_radio(data)
		self.enable_forward(True)

	def get_selected_data(self):
		for i in self.radio:
			if i.GetValue():
				return self.get_data_by_id(i.GetId())

	def get_data_by_id(self, id):
		for data in self.providers.values():
			if data['id'] == id:
				return data
		raise IndexError, 'ID is not present in provider list'

	def pick_radio(self, data):
		module = '.'.join(data['next'].split('.')[:-1])
		cls = data['next'].split('.')[-1]
		if self.next:
			self.next.__del__()
		self.next = getattr(importlib.import_module(module), cls)(self.GetParent())
		self.next.prev = self

	def dump_config(self, config):
		data = self.get_selected_data()
		config.add_section('main')
		config.set('main', 'target', data['provider'])