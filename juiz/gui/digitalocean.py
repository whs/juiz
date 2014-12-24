from libcloud.compute.types import Provider
from .BaseWizardPage import WizardInputListPage
from .CloudConfigPage import CloudConfigPage

CONFIG_SECTION = 'target:{0}'.format(Provider.DIGITAL_OCEAN)

class DOCloudConfigWizardPage(WizardInputListPage):
	fields = ['Client ID', 'API Key']
	help_text = 'Only v1 API key is supported'
	hyperlink = {
		'API Key Management': 'https://cloud.digitalocean.com/api_access'
	}

	def __init__(self, *args, **kwargs):
		super(DOCloudConfigWizardPage, self).__init__(*args, **kwargs)
		self.set_next(DOCloudConfigPage(*args, **kwargs))

	def get_settings(self):
		data = self.get_values_dict()
		return {
			'key': data['client_id'],
			'secret': data['api_key']
		}

	def dump_config(self, config):
		config.add_section(CONFIG_SECTION)
		
		for k, v in self.get_settings().iteritems():
			config.set(CONFIG_SECTION, k, v)

class DOCloudConfigPage(CloudConfigPage):
	fields = ['Location', 'Size']
	provider = Provider.DIGITAL_OCEAN