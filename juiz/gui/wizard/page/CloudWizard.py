import wx

from libcloud.compute.types import Provider

from juiz import util
from .BaseWizardPage import BaseWizardPage

class CloudPickProviderWizardPage(BaseWizardPage):
	providers = {
		'Amazon Elastic Compute Cloud (EC2)': {
			'id': 5001,
			'next': 'juiz.gui.provider.aws.AWSCloudConfigWizardPage',
			'provider': Provider.EC2
		},
		'DigitalOcean': {
			'id': 5002,
			'next': 'juiz.gui.provider.digitalocean.DOCloudConfigWizardPage',
			'provider': Provider.DIGITAL_OCEAN
		},
		'CloudStack': {
			'id': 5003,
			'provider': Provider.CLOUDSTACK,
			'next': 'juiz.gui.provider.cloudstack.CloudStackCloudConfigWizardPage',
		},
		# 'OpenStack': {
		# 	'id': 5004,
		# 	'provider': Provider.OPENSTACK,
		# },
	}

	def __init__(self, parent):
		super(CloudPickProviderWizardPage, self).__init__(parent)
		outer_sizer = wx.BoxSizer(wx.VERTICAL)
		help_text = wx.StaticText(self, -1, _('Select cloud provider to configure:'))
		help_text.Wrap(parent.GetPageSize().width)
		outer_sizer.Add(help_text, 0, wx.EXPAND)
		outer_sizer.AddSpacer(10)

		self.radio = []

		for k,v in self.providers.items():
			self.create_radio(_(k), v['id'])

		for radio in self.radio:
			outer_sizer.Add(radio, 0, wx.EXPAND)
			outer_sizer.AddSpacer(2)
		
		self.SetSizer(outer_sizer)

		parent.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, self.on_show)
		self.Bind(wx.EVT_RADIOBUTTON, self.radio_change)

	def on_show(self, event):
		if event.GetPage() == self:
			self.enable_forward(True)
		event.Skip()

	__is_first = True

	def create_radio(self, name, id=wx.ID_ANY):
		radio = wx.RadioButton(self, id, name)
		project = self.get_project()
		data = self.get_data_by_id(id)
		if project:
			if project.config.get('main', 'target') == data['provider']:
				radio.SetValue(True)
				self.pick_radio(data)
		elif self.__is_first:
			self.__is_first = False
			radio.SetValue(True)
			self.pick_radio(data)
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
		self.next = util.import_by_name(data['next'])(self.GetParent())
		self.next.prev = self

	def dump_config(self, config):
		data = self.get_selected_data()
		config.set('main', 'target', data['provider'])